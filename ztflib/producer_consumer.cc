#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <iostream>


class Queue
{
public:
    void put(int val)
    {
        std::unique_lock<std::mutex> lck(mtx_);
        while(queue_.size() >= 3)
        {
            cdv_.wait(lck);//主动阻塞，主动等待,cdv_调用lck的lock()和unlock()方法
        }
        //等价于
        //cdv.wait(lck, [](){ return !queue_.empty() })
        queue_.push(val);
        cdv_.notify_all();//通知其他线程，唤醒其他线程，去获取互斥锁
    }
    int get()
    {
        std::unique_lock<std::mutex> lck(mtx_);
        while (queue_.empty())
        {
            cdv_.wait(lck);//主动阻塞，主动等待，cdv_调用lck的lock()和unlock()方法
        }
        //等价于
        //cdv.wait(lck, [](){ return queue_.empty() })
        int front = queue_.front();
        queue_.pop();
        cdv_.notify_all();
        return front;
    }
private:
    std::queue<int> queue_;
    std::mutex mtx_;
    std::condition_variable cdv_;
};

//生产者线程
void producer(Queue *q)
{
    for(int i =0 ;i<10;++i)
    {
        q->put(i);
        std::cout<<"put "<< i <<std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    q->put(666);
}

//消费者线程
void constumer(Queue *q)
{
    while(true)
    {
      int v = q->get();
      if(v == 666)break;
      std::cout<<"get "<<v<<std::endl;
      std::this_thread::sleep_for(std::chrono::seconds(4));
    }
}

int main()
{
    Queue q;
    std::thread t1(producer,&q);
    std::thread t2(constumer,&q);

    t1.join();
    t2.join();
    return 0;
}
