#include "Notify.h"

/// NotifyImpl Implementation
NotifyImpl::NotifyImpl()
{    
}

NotifyImpl::~NotifyImpl()
{    
}

void NotifyImpl::notify(int id, std::string title, std::string message, unsigned long delay, bool repeat, int priority)
{
	printf("%d:%s:%s:%lu:%d:%d", id, title.c_str(), message.c_str(), delay, repeat, priority);
}