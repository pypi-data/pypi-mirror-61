/// notify
PyDoc_STRVAR(notify_doc,
    "Register a notification with the system.\n"\
    "\n"\
    "\n"\
    "notify(id, title, message, delay, repeat, priority);\n"\
    "\n"\
    "Parameters\n"\
    "----------\n"\
    "    id : int\n"\
    "        The notification id, must be > 0, notify new message with the same 'id' will override the old one.\n"\
    "    title : string\n"\
    "        The title of the notification.\n"\
    "    message : string\n"\
    "        The notification message\n"\
    "    delay : unsigned long (optional)\n"\
    "        Delay the notification with timer, in miliseconds.\n"\
    "        Default: 30000ms \n"\
    "    repeat : int (optional)\n"\
    "        Set to 1 if this is repeatable message. If set, 'delay' param will act as interval. Min interval is 900000ms, or 15m.\n"
    "        Default: 0.\n"
    "    priority : int (optional)\n"\
    "        Max = 2, High = 1, Med = 0, Low = -1, Min = -2.\n"
    "        Default: 0.\n"
);
