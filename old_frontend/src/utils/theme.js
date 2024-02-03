import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
    palette: {
        primary: {
            light: '#2d5f99',
            main: '#0a314d',
            dark: '#062135',
            contrastText: '#fff',
        },
        secondary: {
            light: '#e31c3d',
            main: '#c1a783',
            dark: '#981b1e',
            contrastText: '#000',
        },
    },
});