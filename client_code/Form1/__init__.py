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
  list_price = ""
  cost_after = ""
  freight = ""
  misc = ""
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
    self.full_list = [(row["Part Number"], row) for row in app_files.liftmaster_all_items["Sheet1"].rows]
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
    self.misc_check.checked = True
    self.markup_check.checked = True

    """Getting the product info from the spreadsheet"""
    part_selected = self.part_look_up.selected_value
    self.item_number = part_selected['Part Number']
    self.item_description = part_selected['Description']
    self.list_price = part_selected['List Price']
    self.item_amount.text = 1
    self.markup_percentage.text = 60

    """Set the amounts into the displayed text to veiw"""
    self.item_description_text.text = self.item_description
    self.list_price_box.text = self.list_price
    self.misc_amount.text = 100
    self.freight_amount.text = 200
    self.weld_charge_amount.text = 45
    self.prep_cost_amount.text = 65
    self.pipe_amount.text = 6.95
    self.total_cost_box.text = "$ " + '{:,.2f}'.format(float(self.list_price.lstrip('$ ').rstrip(' ').replace(",", "")) + 416.95)
    self.markup_box.text = "$ " + '{:,.2f}'.format((float(self.list_price.lstrip('$ ').rstrip(' ').replace(",", "")) + 416.95)*0.6)
    self.unit_price_box.text = "$ " + '{:,.2f}'.format(float(self.list_price.lstrip('$ ').rstrip(' ').replace(",", "")) + 416.95 + ((float(self.list_price.lstrip('$ ').rstrip(' ').replace(",", "")) + 416.95)*0.6))
    self.extended_price_box.text = self.unit_price_box.text
    
    """Get extended price as a float for adding to total"""
    self.extended_price = float(self.list_price.lstrip('$ ').rstrip(' ').replace(",", "")) + 416.95 + (float(self.list_price.lstrip('$ ').rstrip(' ').replace(",", "")) + 416.95)*0.6

  def set_selling(self):
    """Float variables to total up costs"""
    total_cost_float = float(self.list_price.lstrip('$ ').rstrip(' ').replace(",", ""))
    unit_price_float = float(self.list_price.lstrip('$ ').rstrip(' ').replace(",", ""))

    """If freight is checked add it to the totals"""
    if self.freight_check.checked:
      unit_price_float += float(self.freight_amount.text)
      total_cost_float += float(self.freight_amount.text)

    """If misc is checked add it to the totals"""
    if self.misc_check.checked:
      unit_price_float += float(self.misc_amount.text)
      total_cost_float += float(self.misc_amount.text)

    """If weld charge is checked add it to the totals"""
    if self.weld_charge_check.checked:
      unit_price_float += float(self.weld_charge_amount.text)
      total_cost_float += float(self.weld_charge_amount.text)

    """If prep cost is checked add it to the totals"""
    if self.prep_cost_check.checked:
      unit_price_float += float(self.prep_cost_amount.text)
      total_cost_float += float(self.prep_cost_amount.text)

    """If pipe is checked add it to the totals"""
    if self.pipe_check.checked:
      unit_price_float += float(self.pipe_amount.text)
      total_cost_float += float(self.pipe_amount.text)

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
    self.part_look_up.items = [(row["Part Number"], row) for row in app_files.liftmaster_all_items["Sheet1"].rows]
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
  
  def call_search_list(self, **event_args):
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
    self.part_look_up.items = [(row["Part Number"], row) for row in app_files.liftmaster_all_items["Sheet1"].rows]
    self.invoice_number_item = self.part_look_up.selected_value
    self.rich_text_2.content = 'DATE ' + date.today().strftime("%B %d, %Y") + '\n' + 'NUMBER ' + self.invoice_number_item['Invoice Number']
    pass

  def call_set_selling(self, **event_args):
    self.set_selling()
    pass
