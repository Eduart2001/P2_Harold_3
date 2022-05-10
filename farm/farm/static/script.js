function copyFunctionNumber() {
  navigator.clipboard.writeText("0356/55 12 25");

  var tooltip = document.getElementById("myTooltip");
  tooltip.innerHTML = "Phone numer copied";
}
function copyFunctionEmail() {
  navigator.clipboard.writeText("ferme3chenes@cows.be");

  var tooltip = document.getElementById("myTooltip2");
  tooltip.innerHTML = "Email copied";
}
function outFunc() {
  var tooltip = document.getElementById("myTooltip");
  tooltip.innerHTML = "Copy to clipboard";
}
function update() {
  /* the update function is the function that handles the requests from the web site to the database, and vice versa.
      it uses ajax to collect data when the button Show is clicked, and stores it in the #form request data label when this request is 
      done with success, it tries  to decompose the string sent from the db to the ajax form as dictionary  in two arrays keys and values,
      after that it calls the chart_creation(id,keys,values) which updates the data of the chart on to the new ones.
      if an error occurred during this request, like missing data to generate the chart, it decomposes the string error in to an array 
      and for each element of the error array it makes their border red by calling the function missingData(element).
    */
  var chartSelector = document.getElementById("chart-select");
  var selectedChart = chartSelector.value;
  //chart_creation(selectedChart)
  $(document).ready(function () {
    $("#form").on("submit", function (e) {
      $.ajax({
        data: {
          chartId: $("#chart-select").val(),
          start_month: $("#start-month-select").val(),
          start_year: $("#start-year-select").val(),
          end_month: $("#end-month-select").val(),
          end_year: $("#end-year-select").val(),
          family_filter: $("#family-select").val(),
          chartId: $("#chart-select").val(),
          fullMoon: $("#fullmoon-select").val(),
          raceType1: $("#raceType1-select").val(),
          raceType2: $("#raceType2-select").val(),
          raceType3: $("#raceType3-select").val(),
          percentage: $("#percentage-select").val(),
        },
        type: "POST",
        url: "/charts",
      }).done(function (data) {
        try {
          //Transformin jsonify dictionnary to array
          var keys = data.keys
            .replace("dict_keys([", "")
            .replace("])", "")
            .split(",");
          //Transformin jsonify dictionnary to array
          var values = data.values
            .replace("dict_values([", "")
            .replace("])", "")
            .split(",");

          chart_creation(selectedChart, keys, values);
        } catch {
          var values = data.error
            .replace("dict_values(", "")
            .replace(",)", "")
            .replace(")", "")
            .split(",")
            .reverse();
          console.log(values);
          for (var x in values) {
            missingData(values[x]);
          }
          console.log("ERROR");
        }
      });
      e.preventDefault();
    });
  });
}
function missingData(name) {
  /* makes the border of the name element red */
  var css_error = {
    border: "2px solid red",
    "border-radius": " 8px",
  };
  $("#" + name).css(css_error);
}
function chart_creation(chart_type, keys, values) {
  //generates random colors for the chart bars
  var Col_array = [];
  for (var x in keys) {
    var r = () => (Math.random() * 256) >> 0;
    var color = `rgb(${r()}, ${r()}, ${r()}, 0.5)`;
    Col_array.push(color);
  }

  /*
    depending on the chart-to-display selection it updates the attributes of the chart created before
    */
  if (chart_type == 0) {
    chart.type = "bar";
    chart.data.labels = keys;
    chart.data.datasets = [
      {
        label: "Cows born over the decades",
        data: values,
        backgroundColor: [
          //couleur du fond des batonets
          "rgba(255, 99, 132, 0.2)", //red (red, green, blue, transparency)
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 206, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgba(153, 102, 255, 0.2)",
          "rgba(255, 159, 64, 0.2)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)", //les bords des batonets
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
        ],
        borderWidth: 1, //épaiseur des bords
      },
    ];
    chart.update();
  } else if (chart_type == 1) {
    chart.type = "bar";
    chart.data.labels = keys;
    chart.data.datasets = [
      {
        label: "Vêlages",
        data: values,
        backgroundColor: Col_array,
        borderColor: Col_array,
        borderWidth: 1, //épaiseur des bords
      },
    ];
    chart.update();
  } else if (chart_type == 2) {
    chart.type = "bar";
    chart.data.labels = keys;
    chart.data.datasets = [
      {
        label: "Animaux nés",
        data: values,
        backgroundColor: Col_array,
        borderColor: Col_array,
        borderWidth: 1, //épaiseur des bords
      },
    ];
    chart.update();
  } else if (chart_type == 3) {
    chart.type = "bar";
    chart.data.labels = keys;
    chart.data.datasets = [
      {
        label: "Vaches",
        data: values,
        backgroundColor: Col_array,
        borderColor: Col_array,
        borderWidth: 1, //épaiseur des bords
      },
    ];
    chart.update();
  }
}
function changeLanguage() {
  //change the text of the website based on a dictionary that contains their traduction
  location.hash = languageSwitcher.textContent;
  change_language(location.hash);
}
function chartSelectChange() {
  //when chart-select is changed hide and show the wanted selects that are attributed to the specific chart
  $("#chart-select").on("change", function () {
    var selectValue = $(this).val();
    var css_changes = {
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    };
    if (selectValue == 1) {
      $("#start-month-select").show().css(css_changes);
      $("#end-month-select").show().css(css_changes);
      $("#start-year-select").show().css(css_changes);
      $("#end-year-select").show().css(css_changes);
      $("#family-select").show().css(css_changes);
      $("#fullmoon-select").hide().css(css_changes);
      $("#raceType1-select").hide().css(css_changes);
      $("#raceType2-select").hide().css(css_changes);
      $("#raceType3-select").hide().css(css_changes);
      $("#percentage-select").hide().css(css_changes);
    } else if (selectValue == 2) {
      $("#start-month-select").show().css(css_changes);
      $("#start-year-select").show().css(css_changes);
      $("#end-month-select").hide().css(css_changes);
      $("#end-year-select").hide().css(css_changes);
      $("#family-select").show().css(css_changes);
      $("#fullmoon-select").show().css(css_changes);
      $("#raceType1-select").hide().css(css_changes);
      $("#raceType2-select").hide().css(css_changes);
      $("#raceType3-select").hide().css(css_changes);
      $("#percentage-select").hide().css(css_changes);
    } else if (selectValue == 3) {
      $("#start-month-select").hide().css(css_changes);
      $("#end-month-select").hide().css(css_changes);
      $("#start-year-select").hide().css(css_changes);
      $("#end-year-select").hide().css(css_changes);
      $("#family-select").hide().css(css_changes);
      $("#fullmoon-select").hide().css(css_changes);
      $("#raceType1-select").show().css(css_changes);
      $("#raceType2-select").show().css(css_changes);
      $("#raceType3-select").show().css(css_changes);
      $("#percentage-select").show().css(css_changes);
    } else {
      $("#start-month-select").hide().css(css_changes);
      $("#end-month-select").hide().css(css_changes);
      $("#start-year-select").hide().css(css_changes);
      $("#end-year-select").hide().css(css_changes);
      $("#family-select").hide().css(css_changes);
      $("#fullmoon-select").hide().css(css_changes);
      $("#raceType1-select").hide().css(css_changes);
      $("#raceType2-select").hide().css(css_changes);
      $("#raceType3-select").hide().css(css_changes);
      $("#percentage-select").hide().css(css_changes);
    }
  });
}
function startMonthSelectChange() {
  $("#start-month-select").on("change", function () {
    //Verify that the selected months are correct start date cant be older that end date
    var monthSelector = document.getElementById("start-month-select").value;
    var endMonthSelector = document.getElementById("end-month-select").value;
    //year variables
    var yearSelector = document.getElementById("start-year-select").value;
    var endYearSelector = document.getElementById("end-year-select").value;
    $("#start-month-select").css({
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    });
    if (endYearSelector <= yearSelector) {
      if (endMonthSelector <= monthSelector) {
        document.querySelector("#start-month-select").value = endMonthSelector;
      }
      document.querySelector("#start-year-select").value = endYearSelector;
    }
  });
}
function endMonthSelectChange() {
  $("#end-month-select").on("change", function () {
    //Verify that the selected months are correct start date cant be older that end date
    var monthSelector = document.getElementById("start-month-select").value;
    var endMonthSelector = document.getElementById("end-month-select").value;
    //year variables
    var yearSelector = document.getElementById("start-year-select").value;
    var endYearSelector = document.getElementById("end-year-select").value;
    $("#end-month-select").css({
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    });
    if (endYearSelector <= yearSelector) {
      if (endMonthSelector <= monthSelector) {
        document.querySelector("#start-month-select").value = endMonthSelector;
      }
      document.querySelector("#start-year-select").value = endYearSelector;
    }
  });
}
function startYearSelectChange() {
  $("#start-year-select").on("change", function () {
    //Verify that the selected years are correct start date cant be older that end date
    var monthSelector = document.getElementById("start-month-select").value;
    var endMonthSelector = document.getElementById("end-month-select").value;
    //year variables
    var yearSelector = document.getElementById("start-year-select").value;
    var endYearSelector = document.getElementById("end-year-select").value;
    $("#start-year-select").css({
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    });
    if (endYearSelector <= yearSelector) {
      if (endMonthSelector <= monthSelector) {
        document.querySelector("#start-month-select").value = endMonthSelector;
      }
      document.querySelector("#start-year-select").value = endYearSelector;
    }
  });
}
function endYearSelectChange() {
  $("#end-year-select").on("change", function () {
    //Verify that the selected months are correct start date cant be older that end date
    var monthSelector = document.getElementById("start-month-select").value;
    var endMonthSelector = document.getElementById("end-month-select").value;
    //year variables
    var yearSelector = document.getElementById("start-year-select").value;
    var endYearSelector = document.getElementById("end-year-select").value;
    //removes the red border from the #end-year-select when clicked
    $("#end-year-select").css({
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    });
    if (endYearSelector <= yearSelector) {
      if (endMonthSelector <= monthSelector) {
        document.querySelector("#start-month-select").value = endMonthSelector;
      }
      document.querySelector("#start-year-select").value = endYearSelector;
    }
  });
}
function fullMoonSelectChange() {
  $("#fullmoon-select").on("change", function () {
    //removes the red border from the #fullmoon-select when clicked
    $("#fullmoon-select").css({
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    });
  });
}
function percentageSelectChange() {
  $("#percentage-select").on("change", function () {
    //removes the red border from the #percentage-select when clicked
    $("#percentage-select").css({
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    });
  });
}
function raceType1SelectChange() {
  $("#raceType1-select").on("change", function () {
    //removes the red border from all raceTypeX-select when the #raceType1-select clicked
    $("#raceType1-select").css({
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    });

    $("#raceType2-select").css({
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    });
    $("#raceType3-select").css({
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    });
  });
}
function raceType2SelectChange() {
  $("#raceType2-select").on("change", function () {
    //removes the red border from all raceTypeX-select when the #raceType2-select clicked
    $("#raceType1-select").css({
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    });
    $("#raceType2-select").css({
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    });
    $("#raceType3-select").css({
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    });
  });
}
function raceType3SelectChange() {
  $("#raceType3-select").on("change", function () {
    //removes the red border from all raceTypeX-select when the #raceType3-select clicked
    $("#raceType1-select").css({
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    });
    $("#raceType2-select").css({
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    });
    $("#raceType3-select").css({
      "border-radius": "8px",
      padding: "10px",
      border: "2px solid #4CAF50",
    });
  });
}
function change_language(hash) {
  // Define the language reload anchors
  var language = {
    fr: {
      farm: "La Ferme",
      service: "Services",
      type: "Types d' animaux",
      graphic: "Graphiques",
      lang: "En",
      button: "Afficher",
      selection1: "Choisissez un graphique",
      selection2: "Choisissez un mois",
      selection3: "Choisissez une année",
      selection4: "Choisissez un mois",
      selection5: "Choisissez une année",
      selection6: "Choisissez une famille",
      selectionMonth1: "Janvier",
      selectionMonth2: "Février",
      selectionMonth3: "Mars",
      selectionMonth4: "Avril",
      selectionMonth5: "Mai",
      selectionMonth6: "Juin",
      selectionMonth7: "Juillet",
      selectionMonth8: "Août",
      selectionMonth9: "Septembre",
      selectionMonth10: "Octobre",
      selectionMonth11: "Novembre",
      selectionMonth12: "Décembre",
      theFarmText:
        "Notre ferme, la ferme des trois Chênes a fêté l'année passée son 150ème anniversaire. De génération en génération, elle est transmise et entretenue de père en fils et nous faisons tout notre possible pour répondre aux besoins des locaux.",
      servicesText:
        "Dans notre ferme, principalement laitière, nous proposons différents produits et services. Nous proposons du lait frais tous les matins mais également différentes sortes de fromages pour tous les goûts (sur demande). \r\n En été vous pouvez également acheter des oeufs du jour, venez tôt car le stock est limité. De plus nous proposons un service de livraison à domicile, n'hésitez pas à appeler le numéro qui se trouve dans la partie contact du site si vous voulez en bénéficier.",
      animalTypesText:
        "Dans notre modeste ferme on peut trouver trois races de vaches. Nous avons des Holstein, Jersey et des Blanc Bleu Belge. Grâce à une base de données que nous tenons à jour depuis les années 90, nous disposons d'une grande quantité d'informations sur toutes les vaches qui sont passées par cette ferme. Si ça vous intéresse vous pouvez retrouver sur ce site des graphiques interactifs reprenant ces données. Nous avons également un petit poulailler mais ce n'est pas notre élevage principal.",
      chartText:
        "Dans cette section il y a différents graphiques interactifs mettant en avant plusieurs catégories de données. Notre page web est dynamique et responsable de l’extraction de données pertinentes de la base de données, du calcul de quantités pertinentes à l’exploitation des trois chênes, et de l’affichage du résultat par un graphique.",
      contactText:
        "Pour nous joindre : - tel 0356/55 12 25 - email : ferme3chenes@cows.be Nous ferons de notre mieux pour vous répondre au plus vite.",
      farmtit: "La Ferme",
      animaltypestit: "Types d' animaux",
      charttitletit: "Graphiques",
      premierGraph:
        "Le premier  graphique affiche le nombre de vêlages par jour sur une période. On donne l’option à l’utilisateur d’affiner sa recherche en utilisant le champ famille qui est optionnel.",
      deuxiemeGraph:
        "Le deuxième affiche pour une année ou un mois, les animaux nés en période de pleine lune et ceux en nés en dehors. L’option est donnée à l’utilisateur d’affiner sa recherche en utilisant le champ famille qui est optionnel.",
      troisiemeGraph:
        "Le troisième et dernier graphique affiche la distribution des races dans la base de données. On demande en entrée plusieurs races ainsi que le pourcentage minimum de ces dernières et on affiche sur le graphe le nombre d’animaux respectant ces critères par race.",
      chartText2:
        "N'hésitez pas à les consulter pour en apprendre plus sur notre ferme.",
      selection7: "Choisissez une option",
      selection71: "Pleine lune",
      selection72: "Autre",
      selection73: "Tous les deux",
      selection8910: "Choisissez la race à afficher",
      selection11: "Choisissez le pourcentage à afficher",
    },
  };

  // Check if a hash value exists in the URL
  if (hash) {
    // Set the content of the webpage
    // depending on the hash values
    if (hash == "#Fr") {
      theFarm.textContent = language.fr.farm;
      services.textContent = language.fr.service;
      types.textContent = language.fr.type;
      charts.textContent = language.fr.graphic;
      languageSwitcher.textContent = language.fr.lang;
      farmtitle.textContent = language.fr.farmtit;
      animaltypestitle.textContent = language.fr.animaltypestit;
      charttitle.textContent = language.fr.charttitletit;
      thefarmlabel.textContent = language.fr.theFarmText;
      serviceslabel.textContent = language.fr.servicesText;
      animaltypeslabel.textContent = language.fr.animalTypesText;
      chartslabel.textContent = language.fr.chartText;
      contactlabel.textContent = language.fr.contactText;
      bouton.textContent = language.fr.button;
      firstGraph.textContent = language.fr.premierGraph;
      secondGraph.textContent = language.fr.deuxiemeGraph;
      thirdGraph.textContent = language.fr.troisiemeGraph;
      chartslabel2.textContent = language.fr.chartText2;
      select1.textContent = language.fr.selection1;
      select2.textContent = language.fr.selection2;
      select3.textContent = language.fr.selection3;
      select4.textContent = language.fr.selection4;
      select5.textContent = language.fr.selection5;
      select6.textContent = language.fr.selection6;
      select21.textContent = language.fr.selectionMonth1;
      select22.textContent = language.fr.selectionMonth2;
      select23.textContent = language.fr.selectionMonth3;
      select24.textContent = language.fr.selectionMonth4;
      select25.textContent = language.fr.selectionMonth5;
      select26.textContent = language.fr.selectionMonth6;
      select27.textContent = language.fr.selectionMonth7;
      select28.textContent = language.fr.selectionMonth8;
      select29.textContent = language.fr.selectionMonth9;
      select210.textContent = language.fr.selectionMonth10;
      select211.textContent = language.fr.selectionMonth11;
      select212.textContent = language.fr.selectionMonth12;
      select41.textContent = language.fr.selectionMonth1;
      select42.textContent = language.fr.selectionMonth2;
      select43.textContent = language.fr.selectionMonth3;
      select44.textContent = language.fr.selectionMonth4;
      select45.textContent = language.fr.selectionMonth5;
      select46.textContent = language.fr.selectionMonth6;
      select47.textContent = language.fr.selectionMonth7;
      select48.textContent = language.fr.selectionMonth8;
      select49.textContent = language.fr.selectionMonth9;
      select410.textContent = language.fr.selectionMonth10;
      select411.textContent = language.fr.selectionMonth11;
      select412.textContent = language.fr.selectionMonth12;
      select7.textContent = language.fr.selection7;
      select71.textContent = language.fr.selection71;
      select72.textContent = language.fr.selection72;
      select73.textContent = language.fr.selection73;
      select8.textContent = language.fr.selection8910;
      select9.textContent = language.fr.selection8910;
      select10.textContent = language.fr.selection8910;
      select11.textContent = language.fr.selection11;
    } else {
      location.reload();
    }
  }
}
