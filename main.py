import flet as ft

def main(page: ft.Page):
    page.title = "Phone Sales & Inventory Tool"
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    # ခေါင်းစဉ်
    title = ft.Text("📱 ဖုန်းအရောင်းအဝယ် စာရင်းကိုင် Tool", size=24, weight=ft.FontWeight.BOLD, color="amber")

    # အချက်အလက် ရိုက်ထည့်ရန် ကွက်လပ်များ
    txt_model = ft.TextField(label="Phone Model (ဥပမာ- Redmi K70)", border_color="amber")
    txt_imei = ft.TextField(label="IMEI နံပါတ်", keyboard_type=ft.KeyboardType.NUMBER, border_color="amber")
    txt_version = ft.TextField(label="Storage / Version (ဥပမာ- 12/256GB)", border_color="amber")
    
    txt_buy_price = ft.TextField(label="ဝယ်ဈေး (ကျပ်)", keyboard_type=ft.KeyboardType.NUMBER, border_color="amber")
    txt_sell_price = ft.TextField(label="ရောင်းဈေး (ကျပ်)", keyboard_type=ft.KeyboardType.NUMBER, border_color="amber")
    txt_qty = ft.TextField(label="အလုံးရေ (Qty)", value="1", keyboard_type=ft.KeyboardType.NUMBER, border_color="amber")

    # Dashboard ပြသမည့် ကတ်ပြားများ
    lbl_total_phones = ft.Text("0 လုံး", size=16, weight=ft.FontWeight.BOLD, color="cyan")
    lbl_total_buy = ft.Text("0 ကျပ်", size=16, weight=ft.FontWeight.BOLD, color="lightblue")
    lbl_total_profit = ft.Text("0 ကျပ်", size=18, weight=ft.FontWeight.BOLD, color="greenaccent")

    # စာရင်းဇယား (Table) တည်ဆောက်ခြင်း
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Model/Version")),
            ft.DataColumn(ft.Text("IMEI")),
            ft.DataColumn(ft.Text("အလုံးရေ")),
            ft.DataColumn(ft.Text("ဝယ်/ရောင်း")),
            ft.DataColumn(ft.Text("အမြတ်/အရှုံး")),
            ft.DataColumn(ft.Text("လုပ်ဆောင်ချက်")),
        ],
        rows=[]
    )

    # စာရင်းချုပ် သိမ်းဆည်းမည့် variable
    summary = {"total_qty": 0, "total_buy": 0, "total_profit": 0}

    # Dashboard စာရင်းများကို Update လုပ်ပေးမည့် Function
    def update_dashboard():
        lbl_total_phones.value = f"{summary['total_qty']:,.0f} လုံး"
        lbl_total_buy.value = f"{summary['total_buy']:,.0f} ကျပ်"
        
        if summary["total_profit"] >= 0:
            lbl_total_profit.value = f"{summary['total_profit']:,.0f} ကျပ် (မြတ်)"
            lbl_total_profit.color = "greenaccent"
        else:
            lbl_total_profit.value = f"{summary['total_profit']:,.0f} ကျပ် (ရှုံး)"
            lbl_total_profit.color = "red"
        page.update()

    # "စာရင်းသွင်းမည်" ခလုတ်နှိပ်လျှင် အလုပ်လုပ်မည့် Function
    def add_phone_record(e):
        if not txt_model.value or not txt_buy_price.value or not txt_sell_price.value:
            return
        
        try:
            buy = float(txt_buy_price.value)
            sell = float(txt_sell_price.value)
            qty = float(txt_qty.value)
            
            total_buy_cost = buy * qty
            profit_per_item = sell - buy
            total_profit_loss = profit_per_item * qty
            
        except ValueError:
            txt_buy_price.error_text = "ဂဏန်းသီးသန့်သာ ရိုက်ပါ"
            page.update()
            return

        # စာရင်းချုပ်ထဲ ပေါင်းထည့်ခြင်း
        summary["total_qty"] += qty
        summary["total_buy"] += total_buy_cost
        summary["total_profit"] += total_profit_loss

        current_qty = qty
        current_buy_cost = total_buy_cost
        current_profit_loss = total_profit_loss

        new_row = ft.DataRow(cells=[])

        # "တစ်ခုချင်းစီ ဖျက်မည်" ခလုတ်နှိပ်လျှင် အလုပ်လုပ်မည့် စနစ်
        def delete_row(e):
            summary["total_qty"] -= current_qty
            summary["total_buy"] -= current_buy_cost
            summary["total_profit"] -= current_profit_loss
            data_table.rows.remove(new_row)
            update_dashboard()

        # အမြတ်/အရှုံး စာသားအရောင်ခွဲခြားခြင်း
        if total_profit_loss >= 0:
            profit_color = "greenaccent"
            profit_text = f"+{total_profit_loss:,.0f}"
        else:
            profit_color = "red"
            profit_text = f"{total_profit_loss:,.0f}"

        # Table Row ထဲသို့ Data များ ထည့်သွင်းခြင်း
        new_row.cells = [
            ft.DataCell(ft.Column([
                ft.Text(txt_model.value, weight=ft.FontWeight.BOLD),
                ft.Text(txt_version.value if txt_version.value else "-", size=12, color="grey")
            ], spacing=2)),
            ft.DataCell(ft.Text(txt_imei.value if txt_imei.value else "-")),
            ft.DataCell(ft.Text(f"{qty:,.0f} လုံး")),
            ft.DataCell(ft.Column([
                ft.Text(f"ဝယ်: {buy:,.0f}", size=12, color="lightblue"),
                ft.Text(f"ရောင်း: {sell:,.0f}", size=12, color="lightgreen")
            ], spacing=2)),
            ft.DataCell(ft.Text(profit_text, color=profit_color, weight=ft.FontWeight.BOLD)),
            ft.DataCell(ft.IconButton(icon=ft.icons.DELETE, icon_color="red", tooltip="ဖျက်မည်", on_click=delete_row))
        ]

        data_table.rows.append(new_row)
        update_dashboard()

        # သွင်းပြီးသား စာသားကွက်လပ်များကို ပြန်ရှင်းထုတ်ခြင်း
        txt_model.value = ""
        txt_imei.value = ""
        txt_version.value = ""
        txt_buy_price.value = ""
        txt_sell_price.value = ""
        txt_qty.value = "1"
        txt_buy_price.error_text = None
        
        page.update()

    # စာရင်းသွင်းမည့် ခလုတ်
    btn_add = ft.ElevatedButton(
        "အရောင်းအဝယ်စာရင်းသွင်းမည်", 
        on_click=add_phone_record, 
        bgcolor="amber", 
        color="black",
        width=250
    )

    # စာရင်းချုပ်ပြသရန် Dashboard Layout
    dashboard = ft.Container(
        content=ft.Column([
            ft.Row([ft.Text("စုစုပေါင်း ရောင်းချရမှု: "), lbl_total_phones]),
            ft.Row([ft.Text("စုစုပေါင်း ဝယ်ဈေး (အရင်း): "), lbl_total_buy]),
            ft.Divider(color="grey"),
            ft.Row([ft.Text("စုစုပေါင်း အမြတ်/အရှုံး: ", size=16, weight=ft.FontWeight.BOLD), lbl_total_profit]),
        ]),
        bgcolor=ft.colors.SURFACE_VARIANT,
        padding=15,
        border_radius=10
    )

    # Component များကို မျက်နှာပြင်ပေါ် နေရာချခြင်း (ကွန်ပျူတာ Screen အကျယ်အတွက် ညှိထားသည်)
    page.add(
        title,
        ft.Divider(height=15, color="transparent"),
        ft.Row([
            ft.Container(content=txt_model, expand=2),
            ft.Container(content=txt_imei, expand=1),
            ft.Container(content=txt_version, expand=1)
        ], spacing=15),
        ft.Row([
            ft.Container(content=txt_buy_price, expand=2),
            ft.Container(content=txt_sell_price, expand=2),
            ft.Container(content=txt_qty, expand=1)
        ], spacing=15),
        ft.Divider(height=10, color="transparent"),
        ft.Row([btn_add], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=25, color="transparent"),
        ft.Text("📊 အရောင်းစာရင်းချုပ် Dashboard", size=16, weight=ft.FontWeight.BOLD, color="cyan"),
        dashboard,
        ft.Divider(height=25, color="transparent"),
        ft.Text("📋 အရောင်းအဝယ်မှတ်တမ်း ဇယားကွက်", size=16, weight=ft.FontWeight.BOLD, color="cyan"),
        ft.Row([data_table], scroll=ft.ScrollMode.AUTO)
    )

# Browser တွင်သုံးရန် view=ft.AppView.WEB_BROWSER ကို ထည့်သွင်းထားပါသည်
ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8585)
