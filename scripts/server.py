from mindmatrix import MindMatrix


def main():
    mm = MindMatrix(enable_plugin=True, enable_builtins=False)
    mm.start_web_server(host="127.0.0.1", port=9527)


if __name__ == "__main__":
    main()
