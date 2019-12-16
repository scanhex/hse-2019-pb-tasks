#include "tsqueue.h"
#include <cassert>

void threadsafe_queue_init(ThreadsafeQueue *q) {
    queue_init(&q->q);
    pthread_mutex_init(&q->mutex, nullptr);
    pthread_cond_init(&q->cond_not_empty, nullptr);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_cond_destroy(&q->cond_not_empty);
    pthread_mutex_destroy(&q->mutex);
    queue_destroy(&q->q);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->mutex);
    queue_push(&q->q, data);
    pthread_mutex_unlock(&q->mutex);
    pthread_cond_signal(&q->cond_not_empty);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->mutex);
    bool was_empty = queue_empty(&q->q);
    if (!was_empty)
        *data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex);
    return !was_empty;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    pthread_mutex_lock(&q->mutex);
    while (queue_empty(&q->q))
        pthread_cond_wait(&q->cond_not_empty, &q->mutex);
    void *res = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex);
    return res;
}
