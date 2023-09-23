from termcolor import colored


def log_messages(string, *args, **kwargs):
    print(colored(f" 🤖💬️ {string}", *args, **kwargs))


if __name__ == '__main__':
    print(colored(f" 🤖💬️ TEST STRINfg", 'red', attrs=['bold']))
