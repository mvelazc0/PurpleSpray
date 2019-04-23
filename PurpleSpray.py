#!/usr/bin/env python
"""
"""

import sys


if __name__ == "__main__":
    from src.core import print_warning, print_status, print_error

    try:
        import src.framework
        src.framework.mainloop()

    except KeyboardInterrupt:
        print("\n")
        print_status("Exiting PurpleSpray.")
        exit()
        sys.exit()

    except Exception as e:
        print_error("[!] DANGER WILL ROBINSON. DANGER WILL ROBINSON. Error has occurred.")
        print_error(("[!] Printing that error. Get that error. You get it: " + str(e)))
