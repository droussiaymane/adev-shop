function quantity_function(number){
  
    new_quantity=document.querySelector("input.input_quantity"+number).value
    
    price=document.querySelector(".amount"+number).innerHTML
    
    total=document.querySelector("td.product-subtotal"+number)
  
    total_new=price*new_quantity
    total.innerHTML='$'+total_new
   
    
}

function remove_model(number){
    a=document.querySelector("a.remove_modal")
    a.href+=number
}