$(document).ready(function(){



    $("#button_submit_article_modification_form").click(function(){

        hide_all_errors();
        sucess=0;

        titre=$("#titre").val();
        paragraphe=$("#paragraphe").val();
        identifiant=$("#identifiant").val();
        auteur=$("#auteur").val();
        date_publication=$("#date_publication").val();


        if(titre==""){
            $("#titre-empty-error").show();
            sucess--;
        }

        if(titre.length>100){

            $("#title-toolong-error").show();
            sucess--;
        }

        if(identifiant==""){
            $("#identifiant-empty-error").show();
            sucess--;
        }

        if(identifiant.length>50){

            $("#identifiant-toolong-error").show();
            sucess--;
        }

        if(auteur==""){
            $("#auteur-empty-error").show();
            sucess--;
        }

        if(auteur.length>100){

            $("#auteur-toolong-error").show();
            sucess--;
        }


        if(!valider_date(date_publication)){
            sucess--;
        }


        if(paragraphe==""){
            $("#paragraphe-empty-error").show();
            sucess--;
        }

        if(paragraphe.length>500){

            $("#paragraphe-toolong-error").show();
            sucess--;
        }

        if(sucess==0){
            $('#form-ajouter-nouveau-article').submit();
        }else {

            $("#titre").val(titre);
            $("#identifiant").val(identifiant);
            $("#auteur").val(auteur);
            $("#date_publication").val(date_publication);
            $("#paragraphe").val(paragraphe);

        }


    });
});


function hide_all_errors(){
    $("#titre-empty-error").hide();
    $("#titre-toolong-error").hide();

    $("#identifiant-empty-error").hide();
    $("#identifiant-toolong-error").hide();

    $("#auteur-empty-error").hide();
    $("#auteur-toolong-error").hide();


    $("#date_publication-empty-error").hide();
    $("#date_publication-format-invalide-error").hide();
    $("#date_publication-invalide-error").hide();

    $("#paragraphe-empty-error").hide();
    $("#paragraphe-toolong-error").hide();

    return;
}

function valider_date(date_publication) {

  if(date_publication==""){
    $("#date_publication-empty-error").show();
  }  

  //regex des date pris d'ici : https://www.regular-expressions.info/dates.html
  let regex = /^(19|20)\d\d[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])$/ ;
  if(!date_publication.match(regex)){
    $("#date_publication-format-invalide-error").show();
    return false;
  }

  let date= date_publication + "T00:00:00";
  date= new Date(date);

  if(isNaN(date)){
    $("#date_publication-invalide-error").show();
    return false;
  }

 

  return true;



}