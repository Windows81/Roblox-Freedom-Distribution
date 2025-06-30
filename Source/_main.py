import signal
import traceback
import launcher

INTERRUPT_MESSAGE = '** RECEIVED Ctrl+C **'

if __name__ == '__main__':
    interrupt_flag = False
    try:
        launcher.read_eval_loop()
    except KeyboardInterrupt:
        print(INTERRUPT_MESSAGE, flush=True)
    except Exception as e:
        traceback.print_exc()
        print(str(e))
