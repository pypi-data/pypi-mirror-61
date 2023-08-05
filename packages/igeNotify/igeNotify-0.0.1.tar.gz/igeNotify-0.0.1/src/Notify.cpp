#include "Notify.h"
#include <cstdio>

/// Event Implementation
Event::Event(int id, std::string title, std::string message, unsigned long delay, bool repeat, int priority)
    : mID(id), mTitle(title), mMessage(message), mDelay(delay), mRepeatable(repeat), mPriority(priority)
{
}

Event::~Event()
{
}


/// NotifyImpl Implementation
void NotifyImpl::notify(const Event& event)
{
    notify(event.mID,
        event.mTitle,
        event.mMessage,
        event.mDelay,
        event.mRepeatable,
        event.mPriority);
}


/// Notify Implementation
Notify::Notify()
{
    mImpl = new NotifyImpl();
}

Notify::~Notify()
{
    delete mImpl;
    mImpl = nullptr;
}

void Notify::notify(const Event& event)
{
    mImpl->notify(event);
}

void Notify::notify(int id, std::string title, std::string message, unsigned long delay, bool repeat, int priority)
{
    mImpl->notify(id, title, message, delay, repeat, priority);
}
