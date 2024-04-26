from PyQtUIkit.themes import KitTheme, KitPalette, builtin_themes

THEMES = {
    'dark': KitTheme({
        'CageWhite': KitPalette('#404347'),
        'CageBlack': KitPalette('#27292B'),
        'FigureWhite': KitPalette('#00000000', text='#DEE8F7'),
        'FigureBlack': KitPalette('#00000000', text='#000000'),
    }, inherit=builtin_themes['Dark'])
}
