$('.article_title').draggable(
                    { 
                        scroll: true,
                        cursor: "move",                        
                        opacity: 0.6                        
                    }
);

$('.options').droppable({
    drop: function( event, ui ) {
        $( this )
            .addClass("ui-state-highlight")
            this.html("DROPPED");
    }
})