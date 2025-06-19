from textool import StreamHandler, log_errors

handle = StreamHandler()


@log_errors
def main(*args, **kwargs):
    print(*args)
    print(kwargs)


if __name__ == "__main__":
    try:
        main(12, hlp=1)
    finally:
        handle.close()
