$(document).ready(function(){




    $("#button_submit_article_modification_form").click(function(){

        hide_all_errors();

        sucess=0;

        titre=$("#titre").val();
        paragraphe=$("#paragraphe").val();



        if(titre==""){
            $("#titre-empty-error").show();
            sucess--;
        }

        if(titre.length>100){

            $("#title-toolong-error").show();
            sucess--;
        }


        if(paragraphe==""){
            $("#paragraphe-empty-error").show();
            sucess--;
        }

        console.log(paragraphe.length)
        if(paragraphe.length>500){
            $("#paragraphe-toolong-error").show();
            sucess--;
        }

        if(sucess==0){
            $('#form-modifier-article').submit();
        }else {

            $("#titre").val(titre);
            $("#pargraphe").val(pargraphe);

        }


    });
});


function hide_all_errors(){

    $("#titre-empty-error").hide();
    $("#titre-toolong-error").hide();
    $("#paragraphe-empty-error").hide();
    $("#paragraphe-toolong-error").hide();

    return;

}