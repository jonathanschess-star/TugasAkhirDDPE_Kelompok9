import flet as ft

from menu import MENU, recommend


def main(page: ft.Page):
    page.title = "Kantin Cepat"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.GREEN_50
    page.padding = 0

    budget_field = ft.TextField(
        label="Budget kamu",
        value="15000",
        prefix=ft.Text("Rp"),
        keyboard_type=ft.KeyboardType.NUMBER,
        border=ft.OutlineInputBorder(border_radius=12),
        expand=True,
    )
    spice_dropdown = ft.Dropdown(
        label="Lagi ingin makan yang...",
        value="Bebas",
        options=[
            ft.DropdownOption(text="Bebas"),
            ft.DropdownOption(text="Pedas"),
            ft.DropdownOption(text="Tidak pedas"),
        ],
        border=ft.OutlineInputBorder(border_radius=12),
        expand=True,
    )

    results = ft.Column(spacing=10, controls=[
        ft.Container(
            padding=18,
            border_radius=16,
            bgcolor=ft.Colors.WHITE,
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.SCHEDULE, color=ft.Colors.GREEN_700, size=25),
                    ft.Column(tight=True, spacing=3, controls=[
                        ft.Text("Waktu istirahat terbatas?", weight=ft.FontWeight.BOLD),
                        ft.Text("Isi dua pilihan, kami bantu pilihkan menu.", color=ft.Colors.GREY_700),
                    ]),
                ],
            ),
        )
    ])

    def format_price(amount: int) -> str:
        return f"Rp{amount:,}".replace(",", ".")

    def menu_card(item, index: int):
        spice_label = "🌶 Pedas" if item.spicy else "Mild"
        return ft.Container(
            padding=12,
            border_radius=16,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, ft.Colors.GREEN_100),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=14,
                controls=[
                    ft.Image(src=item.image, width=92, height=92, fit=ft.BoxFit.COVER, border_radius=12),
                    ft.Column(expand=True, spacing=5, controls=[
                        ft.Text(f"{index}. {item.name}", size=17, weight=ft.FontWeight.BOLD),
                        ft.Text(item.description, size=13, color=ft.Colors.GREY_700),
                        ft.Row(spacing=10, controls=[
                            ft.Text(format_price(item.price), weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800),
                            ft.Text(spice_label, size=12, color=ft.Colors.GREY_700),
                        ]),
                    ]),
                ],
            ),
        )

    def find_food():
        try:
            budget = int((budget_field.value or "").replace(".", "").replace(",", "").strip())
            if budget <= 0:
                raise ValueError
        except ValueError:
            results.controls = [ft.Text("Masukkan budget dalam angka yang lebih dari 0.", color=ft.Colors.ERROR)]
            page.update()
            return

        recommendations, fallback = recommend(budget, spice_dropdown.value or "Bebas")
        if not recommendations:
            cheapest = min(item.price for item in MENU)
            results.controls = [
                ft.Container(
                    padding=18,
                    border_radius=16,
                    bgcolor=ft.Colors.ORANGE_50,
                    content=ft.Text(f"Belum ada menu di budget ini. Menu termurah mulai {format_price(cheapest)}."),
                )
            ]
        else:
            heading = "Pilihan yang cocok buat kamu" if not fallback else "Pilihan sesuai budget"
            description = (
                "Paling sesuai budget dan preferensimu."
                if not fallback
                else "Belum ada yang cocok dengan pilihan pedasmu, jadi ini opsi lain yang masih masuk budget."
            )
            results.controls = [
                ft.Text(heading, size=19, weight=ft.FontWeight.BOLD),
                ft.Text(description, color=ft.Colors.GREY_700),
                *(menu_card(item, index) for index, item in enumerate(recommendations, start=1)),
            ]
        page.update()

    content = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=18,
        controls=[
            ft.Container(
                padding=ft.Padding.symmetric(horizontal=20, vertical=24),
                border_radius=22,
                bgcolor=ft.Colors.GREEN_700,
                content=ft.Column(spacing=8, controls=[
                    ft.Row(spacing=8, controls=[
                        ft.Icon(ft.Icons.RESTAURANT_MENU, color=ft.Colors.WHITE, size=24),
                        ft.Text("KANTIN CEPAT", color=ft.Colors.WHITE, size=13, weight=ft.FontWeight.BOLD),
                    ]),
                    ft.Text("Makan apa\nhari ini?", size=32, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    ft.Text("Temukan pilihan enak tanpa menghabiskan waktu istirahat.", color=ft.Colors.GREEN_50, size=15),
                ]),
            ),
            ft.Container(
                padding=20,
                border_radius=20,
                bgcolor=ft.Colors.WHITE,
                border=ft.Border.all(1, ft.Colors.GREEN_100),
                content=ft.Column(spacing=14, controls=[
                    ft.Text("Cari menu", size=20, weight=ft.FontWeight.BOLD),
                    budget_field,
                    spice_dropdown,
                    ft.Button(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=8,
                            controls=[ft.Icon(ft.Icons.AUTO_AWESOME), ft.Text("Pilihkan menu")],
                        ),
                        on_click=find_food,
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE,
                    ),
                ]),
            ),
            results,
            ft.Text("Menu dan harga bisa disesuaikan dengan kantinmu.", size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
        ],
    )

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Container(
                expand=True,
                alignment=ft.Alignment.TOP_CENTER,
                padding=ft.Padding.symmetric(horizontal=16, vertical=12),
                content=ft.Container(max_width=560, expand=True, content=content),
            ),
        )
    )


ft.run(main)
