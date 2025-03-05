# from django.test import TestCase
#
# # Create your tests here.
# <html>
#     <head>
#         <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
#         <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
#     </head>
#     <body>
# {#        <form method="POST">#}
#     <div class="container">
#         <div class="row">
#             <div class="col-md-12">
#                 <form method="POST">
#                     <div class="form-group row">
#                         {% csrf_token %}
#                         <label class="col-md-2">
#                             <b>Select Food To Add </b>
#                         </label>
#                         <select class="col-md-6 form-control" name="food_consumed" id="food_consumed">
#                             {% for food in foods %}
#                                 <option value="{{food.name}}">{{food.name}}</option>
#                             {% endfor %}
#                         </select>
#                         <button class="btn btn-success" type="submit">Add</button>
#                     </div>
#                 </form>
#             </div>
#         </div>
#     </div>
#
#     <div class="row">
#         <div class="col-md-7">
#             <div >
#                 <h4> Today's Consumption</h4>
#             </div>
#             <table id="table" class="table table-striped table-primary">
#                 <tr class="bg-primary text-white">
#                     <th>Food item</th>
#                     <th>Carbs(gm)</th>
#                     <th>Protein(gm)</th>
#                     <th>Fats(gm)</th>
#                     <th>Calories(Kcal)</th>
#                     <th>Remove item</th>
#
#                 </tr>
#                 {% for c in consumed_food %}
#                     <tr>
#                         <td>{{c.food_consumed.name}}</td>
#                         <td>{{c.food_consumed.carbs}}</td>
#                         <td>{{c.food_consumed.proteins}}</td>
#                         <td>{{c.food_consumed.fats}}</td>
#                         <td>{{c.food_consumed.calories}}</td>
#                         <td><a class="btn btn-danger" href="{% url 'delete' c.id %}">X</td>
#                     </tr>
#
#                 {% endfor %}
#                 <tr>
#                     <td id="name"><b>Total</b></td>
#                     <td id="totalCarbs"><b></b></td>
#                     <td id="totalProteins"><b></b></td>
#                     <td id="totalFats"><b></b></td>
#                     <td id="totalCalories"><b></b></td>
#                 </tr>
#             </table>
#         </div>
#     </div>
#     <div class="container">
#         <div class="row">
#             <div class="col-md-12">
#                 <nav class="navbar navbar-dark bg-primary">
#                     <span class="navbar-brand">Calorie Tracker</span>
#                 </nav>
#             </div>
#         </div>
#
#         <br><br><br>
#
#         <h4>Calorie Goal</h4>
#         <br>
#         <div class="row">
#             <div class="col-md-9 offset-1">
#                 <div class="progress">
#                     <div class="progress-bar" role="progressbar" style="width: 0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="0"></div>
#                 </div>
#             </div>
#         </div>
#         </table>
#         </div>
#
#                 <div class="col-md-5" offset-1>
#                     <div class="">
#                         <h4>Today's breakdown</h4>
#                     </div>
#
#                     <div class="card-header text-white bg-primary">
#                          <h4>Macronutrients breakdown</h4>
#                     </div>
#
#                     <div class="col-md-12">
#                         <canvas id="myChart" width="400" height="400"></canvas>
#
#                     </div>
#                     </div>
#
#                     <div class="col-md-12">
#
#                     </div>
#                 </div>
#             </div>
#         </div>
#         <br><br>
# {#        </form>#}
#     </body>
#     <script>
#         var table = document.getElementById("table");
#         var carbs = 0, proteins=0, fats=0, calories=0;
#         for(var i=1; i<table.rows.length-1;i++){
#             console.log(table.rows[i].cells[1].innerHTML);
#             carbs += parseFloat(table.rows[i].cells[1].innerHTML);
#             carbs = Math.round(carbs);
#             proteins += parseFloat(table.rows[i].cells[2].innerHTML);
#             fats += parseFloat(table.rows[i].cells[3].innerHTML);
#             calories += parseFloat(table.rows[i].cells[4].innerHTML);
#         }
#         console.log(carbs);
#         document.getElementById("totalCarbs").innerHTML = '<b>' + carbs + '(gm)</b>';
#         document.getElementById("totalProteins").innerHTML = proteins;
#
#         document.getElementById("totalFats").innerHTML = fats;
#         document.getElementById("totalCalories").innerHTML = '<b>' + calories + '(kcal)</b>';
#
#         var calPer = (calories/2000)*100;
#          document.getElementsByClassName("progress-bar")[0].setAttribute("style", "width:"+calPer+"%");
#
#         var total = carbs + proteins +fats;
#         var carbsP= Math.round((carbs/total)*100);
#         var proteinsP= Math.round((proteins/total)*100);
#         var fatsP= Math.round((fats/total)*100);
#
#         var ctx = document.getElementById('myChart').getContext('2d');
#         var myChart = new Chart(ctx, {
#             type: 'doughnut',
#             data: {
#                 labels: ['Carbs '+carbsP+'%', 'Proteins '+proteinsP+'%', 'Fats '+fatsP+'%'],
#                 datasets: [{
#                     data: [carbsP, proteinsP, fatsP],
#                     backgroundColor: [
#                         'rgba(255, 99, 132, 0.6)',
#                         'rgba(255, 255, 100, 0.6)',
#                         'rgba(255, 79, 12, 0.6)',
#                     ],
#                     borderColor: [
#                         'rgba(255, 99, 132, 0.9)',
#                         'rgba(255, 255, 100, 0.9)',
#                         'rgba(255, 79, 12, 0.9)',
#                     ],
#                     borderWidth: 1
#                 }]
#             }
#         });
#
#     </script>
#
#     </script>
# </html>
