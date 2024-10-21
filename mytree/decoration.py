class DisplayFormatChanger:
    def __init__(self):
        self.__charfont_changed = False
        self.__charcolor_changed = False
        self.__background_changed = False

    def is_changed(self):
        if (
            self.__charfont_changed
            or self.__charcolor_changed
            or self.__background_changed
        ):
            return True
        return False

    def reset_change(self):
        print("\033[0m", end="")
        self.__charfont_changed = False
        self.__charcolor_changed = False
        self.__background_changed = False

    def set_char_bold(self):
        print("\033[1m", end="")
        self.__charfont_changed = True

    def set_char_fine(self):
        print("\033[2m", end="")
        self.__charfont_changed = True

    def set_char_iteric(self):
        print("\033[3m", end="")
        self.__charfont_changed = True

    def set_char_underline(self):
        print("\033[4m", end="")
        self.__charfont_changed = True

    def set_char_delete(self):
        print("\033[9m", end="")
        self.__charfont_changed = True

    def set_char_black(self):
        print("\033[30m", end="")
        self.__charcolor_changed = True

    def set_char_red(self):
        print("\033[31m", end="")
        self.__charcolor_changed = True

    def set_char_green(self):
        print("\033[32m", end="")
        self.__charcolor_changed = True

    def set_char_yellow(self):
        print("\033[33m", end="")
        self.__charcolor_changed = True

    def set_char_blue(self):
        print("\033[34m", end="")
        self.__charcolor_changed = True

    def set_char_magenta(self):
        print("\033[35m", end="")
        self.__charcolor_changed = True

    def set_char_cyan(self):
        print("\033[36m", end="")
        self.__charcolor_changed = True

    def set_char_white(self):
        print("\033[37m", end="")
        self.__charcolor_changed = True

    def set_char_with_n(self, n: int):
        string = "\033[38;5;" + str(n) + "m"
        print(string, end="")
        self.__charcolor_changed = True

    def reset_char_color(self):
        print("\033[39m", end="")
        self.__charcolor_changed = False

    def set_background_black(self):
        print("\033[40m", end="")
        self.__background_changed = True

    def set_background_Red(self):
        print("\033[41m", end="")
        self.__background_changed = True

    def set_background_green(self):
        print("\033[42m", end="")
        self.__background_changed = True

    def set_background_yellow(self):
        print("\033[43m", end="")
        self.__background_changed = True

    def set_backgound_blue(self):
        print("\033[44m", end="")
        self.__background_changed = True

    def set_background_magenta(self):
        print("\033[45m", end="")
        self.__background_changed = True

    def set_background_cyan(self):
        print("\033[46m", end="")
        self.__background_changed = True

    def set_background_white(self):
        print("\033[47m", end="")
        self.__background_changed = True

    def reset_background(self):
        print("\033[49m", end="")
        self.__background_changed = False

    @staticmethod
    def show_all_color():
        """show available colors"""
        for i in range(256):
            print("\033[48;5;", i, "m", sep="", end="")
            print(" " * 4, end="")
            print("\033[49m", end=" ")
            print("\033[38;5;", i, "m", sep="", end="")
            print(
                "The quick brown fox jumps over the lazy dog",
                "[" + str(i) + "]",
                end=" ",
            )
            print("\033[39m", end="")
            print()


if __name__ == "__main__":
    DisplayFormatChanger.show_all_color()
