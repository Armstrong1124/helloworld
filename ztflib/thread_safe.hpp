#pragma once

#include <atomic>
#include <condition_variable>
#include <list>
#include <mutex>
#include <queue>
#include <shared_mutex>
#include <utility>

#include "class_macro.h"

template <typename T>
class ThreadSafeQueue {
 public:
  explicit ThreadSafeQueue(const std::size_t capacity);
  ~ThreadSafeQueue();
  void Enqueue(const T& element);
  void Enqueue(const T& element, bool* const discard);
  bool Dequeue(T* const element);
  bool GetFront(T* const front);
  bool PopFront();
  std::size_t size() const;
  bool Empty() const;
  void BreakAllWait();
  void Clear();

 private:
  // 0 if no limit
  std::size_t capacity_ = 0;
  std::list<T> queue_;
  std::condition_variable_any cva_;
  std::atomic<bool> wait_all_break_ = {false};
  mutable std::shared_timed_mutex mutex_;

 private:
  DISALLOW_COPY_AND_ASSIGN(ThreadSafeQueue);
};

template <typename T>
ThreadSafeQueue<T>::ThreadSafeQueue(const std::size_t capacity) : capacity_(capacity) {
}

template <typename T>
ThreadSafeQueue<T>::~ThreadSafeQueue() {
  BreakAllWait();
}

template <typename T>
void ThreadSafeQueue<T>::Enqueue(const T& element) {
  std::unique_lock<std::shared_timed_mutex> lock(mutex_);
  queue_.emplace_back(element);
  while (capacity_ > 0 && queue_.size() > capacity_) {
    queue_.pop_front();
  }
  cva_.notify_one();
}

template <typename T>
void ThreadSafeQueue<T>::Enqueue(const T& element, bool* const discard) {
  if (discard == nullptr) {
    return;
  }
  std::unique_lock<std::shared_timed_mutex> lock(mutex_);
  *discard = false;
  queue_.emplace_back(element);
  while (capacity_ > 0 && queue_.size() > capacity_) {
    queue_.pop_front();
    *discard = true;
  }
  cva_.notify_one();
}

template <typename T>
bool ThreadSafeQueue<T>::Dequeue(T* const element) {
  if (element == nullptr) {
    return false;
  }
  std::unique_lock<std::shared_timed_mutex> lock(mutex_);
  if (queue_.empty()) {
    return false;
  }
  *element = std::move(queue_.front());
  queue_.pop_front();
  return true;
}

template <typename T>
std::size_t ThreadSafeQueue<T>::size() const {
  std::shared_lock<std::shared_timed_mutex> lock(mutex_);
  return queue_.size();
}

template <typename T>
bool ThreadSafeQueue<T>::Empty() const {
  std::shared_lock<std::shared_timed_mutex> lock(mutex_);
  return queue_.empty();
}

template <typename T>
bool ThreadSafeQueue<T>::GetFront(T* const front) {
  if (front == nullptr) {
    return false;
  }
  std::shared_lock<std::shared_timed_mutex> lock(mutex_);
  if (queue_.empty()) {
    return false;
  }
  *front = queue_.front();
  return true;
}

template <typename T>
bool ThreadSafeQueue<T>::PopFront() {
  std::unique_lock<std::shared_timed_mutex> lock(mutex_);
  if (queue_.empty()) {
    return false;
  }
  queue_.pop_front();
  return true;
}

template <typename T>
void ThreadSafeQueue<T>::BreakAllWait() {
  wait_all_break_ = true;
  cva_.notify_all();
}

template <typename T>
void ThreadSafeQueue<T>::Clear() {
  std::unique_lock<std::shared_timed_mutex> lock(mutex_);
  while (!queue_.empty()) {
    queue_.pop_front();
  }
}