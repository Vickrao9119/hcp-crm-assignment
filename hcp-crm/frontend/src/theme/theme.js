import { createTheme } from "@mui/material/styles";
import { palette, fonts } from "./palette";

/**
 * Builds an MUI theme for either 'light' or 'dark' mode using our design tokens.
 */
export const buildTheme = (mode = "light") =>
  createTheme({
    palette: {
      mode,
      primary: {
        main: palette.primary,
        dark: palette.primaryDark,
        light: palette.primaryLight,
      },
      secondary: { main: palette.accent },
      warning: { main: palette.warning },
      error: { main: palette.danger },
      background: {
        default: mode === "light" ? palette.bgLight : palette.bgDark,
        paper: mode === "light" ? palette.bgLightAlt : palette.bgDarkAlt,
      },
      text: {
        primary: mode === "light" ? palette.textDark : "#EAF1F5",
        secondary: palette.textMuted,
      },
      divider: mode === "light" ? palette.border : "rgba(255,255,255,0.08)",
    },
    shape: { borderRadius: 14 },
    typography: {
      fontFamily: fonts.body,
      h1: { fontFamily: fonts.display, fontWeight: 600 },
      h2: { fontFamily: fonts.display, fontWeight: 600 },
      h3: { fontFamily: fonts.display, fontWeight: 600 },
      h4: { fontFamily: fonts.display, fontWeight: 600 },
      h5: { fontFamily: fonts.display, fontWeight: 600 },
      h6: { fontFamily: fonts.body, fontWeight: 700 },
      button: { textTransform: "none", fontWeight: 600 },
    },
    components: {
      MuiPaper: {
        styleOverrides: {
          root: { backgroundImage: "none" },
        },
      },
      MuiCard: {
        styleOverrides: {
          root: {
            border: `1px solid ${mode === "light" ? palette.border : "rgba(255,255,255,0.08)"}`,
            boxShadow:
              mode === "light" ? "0 4px 24px rgba(22,75,112,0.06)" : "none",
          },
        },
      },
      MuiButton: {
        styleOverrides: {
          root: { borderRadius: 10, paddingLeft: 18, paddingRight: 18 },
        },
      },
    },
  });
