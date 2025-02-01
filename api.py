

import book

def main():
    print()
    from counter import whileInputValidOptionDict
    option = whileInputValidOptionDict({
        **{usecase : book.reserveRemove for usecase in book.usecasesRemove},
        **{usecase : book.reserveDownload for usecase in book.usecasesDownload},
        **{usecase : book.reserveConvert for usecase in book.usecasesConvert},
        **{usecase : book.reserveShow for usecase in book.usecasesShow},
        **{usecase : book.reserveAlbumArt for usecase in book.usecasesAlbumnArt},
    })
    option[1](option[0])
    print()

main()