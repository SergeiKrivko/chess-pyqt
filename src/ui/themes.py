from PyQtUIkit.themes import KitTheme, KitPalette, builtin_themes

THEMES = {
    'light': KitTheme({
        'CageWhite': KitPalette('#B0B0B0'),
        'CageBlack': KitPalette('#8A8A8A'),
        'FigureWhite': KitPalette('#00000000', text='#FFFFFF'),
        'FigureBlack': KitPalette('#00000000', text='#000000'),
    }, inherit=builtin_themes['Light']),
    'dark': KitTheme({
        'CageWhite': KitPalette('#404347'),
        'CageBlack': KitPalette('#27292B'),
        'FigureWhite': KitPalette('#00000000', text='#DEE8F7'),
        'FigureBlack': KitPalette('#00000000', text='#000000'),
    }, inherit=builtin_themes['Dark'])
}
