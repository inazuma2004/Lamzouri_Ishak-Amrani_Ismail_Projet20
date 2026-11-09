"""Génère les wireframes PNG de la maquette (dossier docs/semaine1/img/).

Les images sont des maquettes statiques destinées au dossier de lancement
de la semaine 1. Elles ne dépendent d'aucune capture d'écran et peuvent être
régénérées à tout moment :

    python scripts/generer_wireframes.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Palette et constantes
# ---------------------------------------------------------------------------
W, H = 1200, 800
BG = "#F3F5F9"
CARD = "#FFFFFF"
BORDER = "#D7DDE8"
TEXT = "#111827"
MUTED = "#6B7280"
ACCENT = "#2563EB"
ACCENT_LIGHT = "#DBEAFE"
GREEN = "#16A34A"
GREEN_LIGHT = "#DCFCE7"
ORANGE = "#D97706"
ORANGE_LIGHT = "#FEF3C7"
RED = "#DC2626"
TABLE_HEAD = "#EEF2FF"

OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "semaine1" / "img"


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Charge une police lisible, avec repli sur la police par défaut."""
    candidates = [
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


F_TITLE = _font(26, bold=True)
F_SUB = _font(15)
F_H2 = _font(18, bold=True)
F_BODY = _font(15)
F_SMALL = _font(13)
F_MONO = _font(13)
F_BADGE = _font(14, bold=True)
F_BIG = _font(34, bold=True)


def rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int = 14,
    fill: str = CARD,
    outline: str | None = BORDER,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paragraph(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font,
    fill: str = TEXT,
    max_width: int = 600,
    line_height: int = 22,
) -> int:
    x, y = xy
    for line in wrap(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return y


def header(draw: ImageDraw.ImageDraw, screen: str) -> None:
    draw.rectangle((0, 0, W, 92), fill="#0F172A")
    draw.text((40, 20), "IT Helpdesk Intelligent", font=F_TITLE, fill="#FFFFFF")
    draw.text(
        (40, 56),
        "Agent autonome de résolution d'incidents IT — maquette semaine 1",
        font=F_SUB,
        fill="#CBD5E1",
    )
    draw.text((W - 250, 34), screen, font=F_SUB, fill="#93C5FD")


def footer(draw: ImageDraw.ImageDraw) -> None:
    draw.line((40, H - 52, W - 40, H - 52), fill=BORDER, width=1)
    draw.text(
        (40, H - 40),
        "Projet 20 — Lamzouri / Amrani — wireframe non contractuel — 09/11/2026",
        font=F_SMALL,
        fill=MUTED,
    )


def badge(draw: ImageDraw.ImageDraw, xy: tuple[int, int], label: str, fg: str, bg: str, width: int = 150) -> None:
    x, y = xy
    draw.rounded_rectangle((x, y, x + width, y + 34), radius=10, fill=bg)
    draw.text((x + 14, y + 8), label, font=F_BADGE, fill=fg)


def progress(draw: ImageDraw.ImageDraw, xy: tuple[int, int], ratio: float, color: str, width: int = 420) -> None:
    x, y = xy
    draw.rounded_rectangle((x, y, x + width, y + 16), radius=8, fill="#E5E7EB")
    draw.rounded_rectangle((x, y, x + int(width * ratio), y + 16), radius=8, fill=color)


def screen1() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, "Écran 1 / 3 — Qualification unitaire")
    footer(d)

    # Carte de saisie
    rounded(d, (40, 120, 560, 730))
    d.text((70, 145), "1. Décrire l'incident", font=F_H2, fill=TEXT)
    d.text((70, 178), "Texte libre reçu par le technicien L1", font=F_SMALL, fill=MUTED)
    rounded(d, (70, 210, 530, 350), radius=10, fill="#F9FAFB", outline=BORDER)
    d.multiline_text(
        (86, 226),
        "VPN client fails to authenticate\nwith error code 403 after password\nchange",
        font=F_BODY,
        fill=TEXT,
        spacing=8,
    )
    rounded(d, (70, 380, 300, 426), radius=10, fill=ACCENT)
    d.text((100, 392), "Prédire la catégorie", font=F_BADGE, fill="#FFFFFF")

    d.text((70, 470), "Entrée", font=F_SMALL, fill=MUTED)
    rounded(d, (70, 492, 530, 560), radius=10, fill="#F9FAFB", outline=BORDER)
    d.text((86, 510), '{"text": "VPN client fails to authenticate..."}', font=F_MONO, fill=TEXT)

    d.text((70, 600), "Traitement", font=F_SMALL, fill=MUTED)
    d.text((70, 625), "1. Nettoyage + vectorisation TF-IDF", font=F_BODY, fill=TEXT)
    d.text((70, 655), "2. LogisticRegression → catégorie + probabilité", font=F_BODY, fill=TEXT)
    d.text((70, 685), "3. Si confiance ML ≥ 0,60 → recherche du runbook", font=F_BODY, fill=TEXT)

    # Carte de résultat
    rounded(d, (600, 120, 1160, 730))
    d.text((630, 145), "2. Résultat de l'agent", font=F_H2, fill=TEXT)
    badge(d, (630, 185), "VALIDE", GREEN, GREEN_LIGHT, width=120)
    d.text((630, 240), "Catégorie prédite", font=F_SMALL, fill=MUTED)
    d.text((630, 262), "Access", font=F_BIG, fill=ACCENT)
    d.text((630, 320), "Score de confiance", font=F_SMALL, fill=MUTED)
    d.text((630, 342), "92,4 %", font=F_H2, fill=TEXT)
    progress(d, (630, 382), 0.924, GREEN, width=460)
    d.text((630, 410), "Seuil d'abstention : 60 % — au-dessus, résolution automatique", font=F_SMALL, fill=MUTED)

    rounded(d, (630, 455, 1130, 690), radius=10, fill="#F9FAFB", outline=BORDER)
    d.text((650, 472), "Procédure suggérée — Runbook Access.md", font=F_H2, fill=TEXT)
    y = 508
    for line in [
        "1. Vérifier le verrouillage du compte dans Active Directory.",
        "2. Réinitialiser le mot de passe (politique de sécurité).",
        "3. Vérifier le client VPN, les certificats et la configuration.",
        "4. Tester depuis un autre réseau pour exclure un blocage local.",
    ]:
        y = paragraph(d, (650, y), line, F_BODY, TEXT, max_width=450, line_height=22) + 8
    d.text((650, 650), "Source citée : data/runbooks/Access.md", font=F_SMALL, fill=MUTED)

    return img


def screen2() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, "Écran 2 / 3 — Alerte d'incertitude")
    footer(d)

    rounded(d, (40, 120, 560, 730))
    d.text((70, 145), "1. Décrire l'incident", font=F_H2, fill=TEXT)
    d.text((70, 178), "Texte ambigu ou trop court", font=F_SMALL, fill=MUTED)
    rounded(d, (70, 210, 530, 350), radius=10, fill="#F9FAFB", outline=BORDER)
    d.multiline_text(
        (86, 226),
        "something is weird with the\noffice computer",
        font=F_BODY,
        fill=TEXT,
        spacing=8,
    )
    rounded(d, (70, 380, 300, 426), radius=10, fill=ACCENT)
    d.text((100, 392), "Prédire la catégorie", font=F_BADGE, fill="#FFFFFF")

    d.text((70, 470), "Ce que voit le technicien", font=F_SMALL, fill=MUTED)
    d.text((70, 495), "• Catégorie pressentie : Miscellaneous", font=F_BODY, fill=TEXT)
    d.text((70, 525), "• Confiance : 41,2 % (< seuil 60 %)", font=F_BODY, fill=TEXT)
    d.text((70, 555), "• Statut : A_VERIFIER", font=F_BODY, fill=ORANGE)
    d.text((70, 585), "• Aucune résolution automatique", font=F_BODY, fill=TEXT)

    rounded(d, (70, 630, 530, 700), radius=10, fill=ORANGE_LIGHT, outline=ORANGE)
    paragraph(
        d,
        (86, 644),
        "Le niveau de confiance est inférieur au seuil de 60 %. "
        "Ce ticket est réorienté vers un technicien humain.",
        F_SMALL,
        ORANGE,
        max_width=420,
        line_height=18,
    )

    rounded(d, (600, 120, 1160, 730))
    d.text((630, 145), "2. Résultat de l'agent", font=F_H2, fill=TEXT)
    badge(d, (630, 185), "A_VERIFIER", ORANGE, ORANGE_LIGHT, width=150)
    d.text((630, 240), "Catégorie pressentie", font=F_SMALL, fill=MUTED)
    d.text((630, 262), "Miscellaneous", font=F_BIG, fill=ORANGE)
    d.text((630, 320), "Score de confiance", font=F_SMALL, fill=MUTED)
    d.text((630, 342), "41,2 %", font=F_H2, fill=TEXT)
    progress(d, (630, 382), 0.412, ORANGE, width=460)
    d.text((630, 410), "Seuil d'abstention : 60 % — en dessous, pas de résolution", font=F_SMALL, fill=MUTED)

    rounded(d, (630, 455, 1130, 690), radius=10, fill="#FFF7ED", outline=ORANGE)
    d.text((650, 472), "Action requise", font=F_H2, fill=ORANGE)
    y = 510
    for line in [
        "Le ticket est transmis à un opérateur humain.",
        "Aucune procédure n'est proposée automatiquement.",
        "Le technicien qualifie manuellement la catégorie.",
        "La décision reste traçée dans le journal des prédictions.",
    ]:
        y = paragraph(d, (650, y), line, F_BODY, TEXT, max_width=450, line_height=22) + 8

    return img


def screen3() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, "Écran 3 / 3 — Traitement par lot CSV")
    footer(d)

    rounded(d, (40, 120, 1160, 300))
    d.text((70, 145), "1. Déposer un fichier CSV de tickets", font=F_H2, fill=TEXT)
    d.text((70, 178), "Colonne attendue : Document (texte de l'incident)", font=F_SMALL, fill=MUTED)
    # zone de dépôt en pointillés
    for x in range(70, 1130, 16):
        d.line((x, 215, min(x + 8, 1130), 215), fill=ACCENT, width=2)
        d.line((x, 285, min(x + 8, 1130), 285), fill=ACCENT, width=2)
    for y in range(215, 285, 16):
        d.line((70, y, 70, min(y + 8, 285)), fill=ACCENT, width=2)
        d.line((1130, y, 1130, min(y + 8, 285)), fill=ACCENT, width=2)
    d.text((430, 240), "Glisser-déposer tickets_nouveaux.csv", font=F_H2, fill=ACCENT)

    # Graphique en barres
    rounded(d, (40, 330, 560, 730))
    d.text((70, 355), "2. Distribution des catégories", font=F_H2, fill=TEXT)
    bars = [
        ("Hardware", 0.35, ACCENT),
        ("Access", 0.25, "#3B82F6"),
        ("HR Support", 0.20, "#60A5FA"),
        ("Storage", 0.12, "#93C5FD"),
        ("Autres", 0.08, "#BFDBFE"),
    ]
    y = 405
    for label, ratio, color in bars:
        d.text((70, y), label, font=F_SMALL, fill=TEXT)
        d.rounded_rectangle((190, y - 2, 520, y + 20), radius=8, fill="#E5E7EB")
        d.rounded_rectangle((190, y - 2, 190 + int(330 * ratio), y + 20), radius=8, fill=color)
        d.text((530, y), f"{int(ratio * 100)} %", font=F_SMALL, fill=MUTED)
        y += 58

    # Tableau des résultats
    rounded(d, (600, 330, 1160, 730))
    d.text((630, 355), "3. Aperçu des résultats", font=F_H2, fill=TEXT)
    cols = [638, 878, 998, 1068]
    d.rectangle((630, 395, 1145, 430), fill=TABLE_HEAD)
    for x, label in zip(cols, ["Description", "Catégorie", "Score", "Statut"]):
        d.text((x, 403), label, font=F_SMALL, fill=TEXT)
    rows = [
        ("Laptop screen flickering black", "Hardware", "95,1 %", "VALIDE"),
        ("Request new mouse and keyboard", "Purchase", "89,4 %", "VALIDE"),
        ("VPN authentication failed", "Access", "92,4 %", "VALIDE"),
        ("Something is weird", "Misc.", "41,2 %", "A_VERIFIER"),
    ]
    y = 440
    for i, (desc, cat, score, status) in enumerate(rows):
        if i % 2 == 0:
            d.rectangle((630, y - 4, 1145, y + 40), fill="#F9FAFB")
        d.text((638, y + 6), desc, font=F_SMALL, fill=TEXT)
        d.text((878, y + 6), cat, font=F_SMALL, fill=TEXT)
        d.text((998, y + 6), score, font=F_SMALL, fill=TEXT)
        color = GREEN if status == "VALIDE" else ORANGE
        d.text((1068, y + 6), status, font=F_SMALL, fill=color)
        y += 52

    rounded(d, (630, 650, 900, 696), radius=10, fill=ACCENT)
    d.text((660, 662), "Télécharger le CSV annoté", font=F_BADGE, fill="#FFFFFF")

    return img


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    screens = {
        "ecran1_qualification.png": screen1(),
        "ecran2_incertitude.png": screen2(),
        "ecran3_batch.png": screen3(),
    }
    for name, image in screens.items():
        path = OUT_DIR / name
        image.save(path, dpi=(144, 144))
        print(f"OK {path} ({image.width}x{image.height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
