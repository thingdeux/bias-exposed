$(document).ready(function() {  
    articles = $('.article_title')
    options = $('.options')
    

    // Turn article elements into draggable elements
    articles.draggable(
        { 
            scroll: true,
            cursor: "move",
            cursorAt: {top: 20, left: 20 },
            opacity: 0.6              
        }
    );

    // Options classes are droppable classes that perform actions
    // When draggables are dropped onto them.
    options.droppable({
        accept: ".article_title",
        hoverClass: "ui-state-highlight",
        tolerance: "pointer"       
    });

    // On drop handlers - ie: What to do when a draggable element
    // Is dropped on a droppable element.
    options.on("drop", function(event, ui) {
        if ($(this).hasClass("reassign")) {
            $.ajax({
                type: "POST",
                url: "reassign",
                data: {
                    article: $(ui.draggable).attr('data-id'),
                    to: $(this).attr('data-id')
                }
            });
        }
        else if ($(this).hasClass("delete")) {                        
            $.ajax({
                type: "POST",
                url: "delete",
                data: {
                    article: $(ui.draggable).attr('data-id')                        
                }
            });               
        }
    });
    
    // Turn the article into a neat lil' round ball, easier
    // To move around and drop on a target.
    articles.on("dragstart", function(event, ui)
    {        
        $(this).addClass("dragging");        
    });
    
});