from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
from datetime import date
import time

class Form1(Form1Template):

  """Initiating variables globally so they can be accesed from multiple functions"""
  item_number = ""
  item_description = ""
  cost_after = ""
  freight = ""
  fin_cost = ""
  total_cost = ""
  markup = ""
  unit_price = ""
  extended_price = ""
  net_amount = ""
  hst = ""
  total_due = ""
  extended_price_float = 0
  net_amount_float = 0
  hst_float = 0
  total_due_float = 0
  markup_percentage_type = 0
  full_list = []
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    """Set the variable to look up items in the spreadsheet"""
    self.full_list = [(row["Part Number"], row) for row in app_files.dd_pricing["Sheet1"].rows]
    self.part_look_up.items = self.full_list
    self.invoice_number_item = self.part_look_up.selected_value
    
    """Set the date and quote/invoice number"""    
    self.rich_text_2.content = 'DATE ' + date.today().strftime("%B %d, %Y") + '\n' + 'NUMBER ' + self.invoice_number_item['Invoice Number']
    
    """Filling the list with blank items for formatting"""
    self.repeating_panel_1.items = [{}]
    for x in range(11):
      self.repeating_panel_1.items.append({})
    
    """Put a blank item into both other repeating panels so there text boxs are there"""
    self.repeating_panel_2.items = [{}]  
    self.repeating_panel_2.items = self.repeating_panel_2.items
    self.repeating_panel_3.items = [{}]  
    self.repeating_panel_3.items = self.repeating_panel_3.items
  # Any code you write here will run before the form opens.

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""

    """Reset check boxes to checked whenever product is changed"""
    self.freight_check.checked = True
    self.fin_cost_check.checked = True
    self.markup_check.checked = True

    """Getting the product info from the spreadsheet"""
    part_selected = self.part_look_up.selected_value
    self.item_number = part_selected['Part Number']
    self.item_description = part_selected['Description']
    list_price = part_selected['Price']
    exchange = part_selected['Exchange']
    self.cost_after = part_selected['COST WITH']
    self.freight = part_selected['FREIGHT']
    self.fin_cost = part_selected['Fin Cost']
    self.total_cost = part_selected['TOTAL']
    self.markup = part_selected['MARK-UP']
    self.item_amount.text = 1
    self.unit_price = part_selected['SELLING PRICE']
    self.markup_percentage.text = 60

    """Set the amounts into the displayed text to veiw"""
    self.item_description_text.text = self.item_description
    self.list_price_box.text = list_price
    self.exchange_box.text = exchange
    self.freight_box.text = self.freight
    self.fin_cost_box.text = self.fin_cost
    self.total_cost_box.text = self.total_cost
    self.markup_box.text = self.markup
    self.unit_price_box.text = self.unit_price
    self.extended_price_box.text = self.unit_price
    
    """Get extended price as a float for adding to total"""
    self.extended_price = float(self.unit_price.lstrip('$ ').rstrip(' ').replace(",", ""))

  def set_selling(self):
    """Float variables to total up costs"""
    total_cost_float = float(self.cost_after.lstrip('$ ').rstrip(' ').replace(",", ""))
    unit_price_float = float(self.cost_after.lstrip('$ ').rstrip(' ').replace(",", ""))

    """If freight is checked add it to the totals"""
    if self.freight_check.checked:
      unit_price_float += float(self.freight.lstrip('$ ').rstrip(' ').replace(",", ""))
      total_cost_float += float(self.freight.lstrip('$ ').rstrip(' ').replace(",", ""))

    """If fin cost is checked add it to the totals"""
    if self.fin_cost_check.checked:
      unit_price_float += float(self.fin_cost.lstrip('$ ').rstrip(' ').replace(",", ""))
      total_cost_float += float(self.fin_cost.lstrip('$ ').rstrip(' ').replace(",", ""))

    """Setting the total cost to display"""
    """:, means put , in tousands .2f means show two decimal places"""
    self.total_cost = "$ " + '{:,.2f}'.format(total_cost_float)
    self.total_cost_box.text = self.total_cost

    """Calculating the markup based on the products markup percentage"""
    markup_float = total_cost_float * float(self.markup_percentage.text)/100


    """Setting the markup value to display"""
    self.markup = "$ " + '{:,.2f}'.format(markup_float)
    self.markup_box.text = self.markup

    """If markup is enabled add to total"""
    if self.markup_check.checked:
      unit_price_float += markup_float

    """Setting the final price to display"""
    self.unit_price = "$ " + '{:,.2f}'.format(unit_price_float)
    self.unit_price_box.text = self.unit_price

    """Setting total price to display"""
    self.extended_price_float = unit_price_float*int(self.item_amount.text)
    self.extended_price = "$ " + '{:,.2f}'.format(self.extended_price_float)
    self.extended_price_box.text = self.extended_price
    pass
      
  def freight_check_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    """Run the function to recalculate the selling price"""
    self.set_selling()
    pass

  def fin_cost_check_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.set_selling()

  def markup_check_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.set_selling()
    pass

  def markup_percentage_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.set_selling()
    pass
    
  def item_amount_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.set_selling()
    pass

  def markup_percentage_change(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.set_selling()
    pass
    
  def item_amount_change(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.set_selling()
    pass

  def markup_percentage_lost_focus(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.set_selling()
    pass
    
  def item_amount_lost_focus(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.set_selling()
    pass
  
  def add_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.set_selling()
    
    """Pop out the 12 blank rows"""
    for x in range(12):
      self.repeating_panel_1.items.pop()
    
    """Add currently selected item to the repeating panel list whether empty or not"""
    try:
      self.repeating_panel_1.items.append({'item_number_spot': self.item_number, 'item_description_spot': self.item_description, 'unit_price_spot': self.unit_price, 'quantity_spot': self.item_amount.text, 'extended_price_spot': self.extended_price}) 
    except AttributeError:
      self.repeating_panel_1.items = [
        {'item_number_spot': self.item_number, 'item_description_spot': self.item_description, 'unit_price_spot': self.unit_price, 'quantity_spot': self.item_amount.text, 'extended_price_spot': self.extended_price}
      ]

    """Add the blank rows back"""
    for x in range(12):
      self.repeating_panel_1.items.append({})
    self.repeating_panel_1.items = self.repeating_panel_1.items
    
    """Recalculate tax and totals and set the labels"""
    self.net_amount_float += self.extended_price_float
    self.net_amount_box.text =  '    $ ' + '{:,.2f}'.format(self.net_amount_float)
    self.hst_float = self.net_amount_float*0.13
    self.hst_box.text =  '    $ ' + '{:,.2f}'.format(self.hst_float)
    self.total_due_float = self.net_amount_float + self.hst_float
    self.total_due_box.text =  '    $ ' + '{:,.2f}'.format(self.total_due_float)
    
    pass

  def generate_invoice_click(self, **event_args):
    """This method is called when the button is clicked"""  
    """Remove the lookup and calclating section from the page"""
    self.form_panel.visible = False
    
    """Print the page"""
    self.call_js('printPage')
    
    """Set the lookup section back to visible"""
    self.form_panel.visible = True
    
    """Add one to the invoice number in excel sheet"""
    self.invoice_number_item['Invoice Number'] = '' + str(int(self.invoice_number_item['Invoice Number'])+1)
    
    """Re-set the list items to set the invoice number to freshly updated one"""
    self.part_look_up.items = [(row["Part Number"], row) for row in app_files.dd_pricing["Sheet1"].rows]
    self.invoice_number_item = self.part_look_up.selected_value
    
    """Set the date and number text again"""
    self.rich_text_2.content = 'DATE ' + date.today().strftime("%B %d, %Y") + '\n' + 'NUMBER ' + self.invoice_number_item['Invoice Number']
    pass

  def clear_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    """Set the quote/invoice repeating panel to be empty and add the initial empty rows"""
    self.repeating_panel_1.items = [{}]
    for x in range(11):
      self.repeating_panel_1.items.append({})
    
    """Reset totals and tex to 0 and put that in their text boxes"""
    self.net_amount_float = 0
    self.net_amount_box.text = '    $ ' + '{:,.2f}'.format(self.net_amount_float)
    self.hst_float = 0
    self.hst_box.text = '    $ ' + '{:,.2f}'.format(self.hst_float)
    self.total_due_float = 0
    self.total_due_box.text = '    $ ' + '{:,.2f}'.format(self.total_due_float)
    pass

  def search_list(self):
    """Make a blank list for search results"""
    searched_list = []
    
    """Add blank row first"""
    searched_list.append(self.full_list[0])
    
    """If the item number contains what is searched"""
    for x in self.full_list:
      if self.search_box.text in x[0] or self.search_box.text in x[0].lower():
        """Add to search results list"""
        searched_list.append(x)

    """Set the drop down to be the search results"""
    self.part_look_up.items = searched_list
    
    pass
  
  def search_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.search_list()
    pass

  def search_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.search_list()
    pass

  def search_box_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    self.search_list()
    pass

  def remove_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    """Remove the 12 blank rows"""
    for x in range(12):
      self.repeating_panel_1.items.pop()
    
    """Remove items extended price from totals and tax"""
    self.net_amount_float -= float(self.repeating_panel_1.items[-1]['extended_price_spot'].lstrip('$ ').rstrip(' ').replace(",", ""))
    self.net_amount_box.text =  '    $ ' + '{:,.2f}'.format(self.net_amount_float)
    self.hst_float = self.net_amount_float*0.13
    self.hst_box.text =  '    $ ' + '{:,.2f}'.format(self.hst_float)
    self.total_due_float = self.net_amount_float + self.hst_float
    self.total_due_box.text =  '    $ ' + '{:,.2f}'.format(self.total_due_float)
    
    """Pop the item to remove"""
    self.repeating_panel_1.items.pop()
    
    """Add back the 12 blank rows"""
    try:
      for x in range(12):
        self.repeating_panel_1.items.append({})
    except AttributeError:
      self.repeating_panel_1.items = [{}]
      for x in range(11):
        self.repeating_panel_1.items.append({})
    self.repeating_panel_1.items = self.repeating_panel_1.items
    pass

  def add_total_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    """Remove the 12 blank rows"""
    for x in range(12):
      self.repeating_panel_1.items.pop()
    
    """Adds number from text box as an item for continuing total"""
    try:
      self.repeating_panel_1.items.append({'item_number_spot': 'Cont.', 'item_description_spot': 'Previous Total', 'unit_price_spot': '', 'quantity_spot': '', 'extended_price_spot': '$ ' + '{:,.2f}'.format(float(self.previous_net_amount.text))})
    except AttributeError:
      self.repeating_panel_1.items = [
        {'item_number_spot': 'Cont.', 'item_description_spot': 'Previous Total', 'unit_price_spot': '', 'quantity_spot': '', 'extended_price_spot': '$ ' + '{:,.2f}'.format(float(self.previous_net_amount.text.replace(",", "")))}
      ]
    
    """Add back the 12 blank rows"""
    try:
      for x in range(12):
        self.repeating_panel_1.items.append({})
    except AttributeError:
      self.repeating_panel_1.items = [{}]
      for x in range(11):
        self.repeating_panel_1.items.append({})
    self.repeating_panel_1.items = self.repeating_panel_1.items
    
    """Add the previous total to the new totals and tax"""
    self.net_amount_float += float(self.previous_net_amount.text)
    self.net_amount_box.text =  '    $ ' + '{:,.2f}'.format(self.net_amount_float)
    self.hst_float = self.net_amount_float*0.13
    self.hst_box.text =  '    $ ' + '{:,.2f}'.format(self.hst_float)
    self.total_due_float = self.net_amount_float + self.hst_float
    self.total_due_box.text =  '    $ ' + '{:,.2f}'.format(self.total_due_float)
    pass

  def set_inoice_number_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    """Set the invoice number in the excel sheet"""
    self.invoice_number_item['Invoice Number'] = '' + str(int(self.new_invoice_number.text))
    
    """Repull the new number from the sheet"""
    self.part_look_up.items = [(row["Part Number"], row) for row in app_files.dd_pricing["Sheet1"].rows]
    self.invoice_number_item = self.part_look_up.selected_value
    self.rich_text_2.content = 'DATE ' + date.today().strftime("%B %d, %Y") + '\n' + 'NUMBER ' + self.invoice_number_item['Invoice Number']
    pass