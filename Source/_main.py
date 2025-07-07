import traceback
import launcher

INTERRUPT_MESSAGE = '** RECEIVED Ctrl+C **'

if __name__ == '__main__':
    try:
        launcher.read_eval_loop()
    except KeyboardInterrupt:
        print(INTERRUPT_MESSAGE)
    except Exception as e:
        traceback.print_exc()
        print(str(e))
