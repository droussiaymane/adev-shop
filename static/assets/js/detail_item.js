color=document.querySelectorAll("button.color_disponnible")

for (let i = 0; i < color.length; i++) {
   color_qs=color[i]
    
   color_qs.addEventListener("click",function(event){
        color_active=document.querySelector("button.color_disponnible.active")
        if (color_active != null ){
            color_active.name= ""
            color_active.classList.remove("active")
        }

        this.name="color_active"
       this.classList.add("active")

   })
}   


sizes=document.querySelectorAll("button.size_disponnible")

for (let i = 0; i < sizes.length; i++) {
   size_qs=sizes[i]
    
   size_qs.addEventListener("click",function(event){
        size_active=document.querySelector("button.size_disponnible.active")
        if (size_active != null ){
            size_active.classList.remove("active")
        }
        
       this.classList.add("active")
   })
}   

 function myfunction(id){
    color_qs=document.querySelector('#color'+id)
    color_active=document.querySelector("button.color_disponnible.active")
        if (color_active != null ){
            color_active.classList.remove("active")
        }
    color_qs.classList.add("active")
}


function color_function(input_color){
    document.getElementById("color").value=input_color
   document.querySelector("strong.default_color").innerHTML=input_color


}

function size_function(input_size){
    document.getElementById("size").value=input_size
    document.querySelector("strong.default_size").innerHTML=input_size

  
    
}
