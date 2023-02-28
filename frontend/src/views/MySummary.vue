<template>
  <div>
    <MyHeader style="padding-top:80px"></MyHeader>
    <div class="chart-container" align="center" style="position: relative; height:85vh; width:100vw">
      <canvas id="stackedBar"></canvas>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'MySummary',
  computed: {
    listNames() {
      return this.$store.getters.listNames
    },
    toggleTrue() {
      return this.$store.getters.toggleTrue
    },
    toggleFalse() {
      return this.$store.getters.toggleFalse
    }
  },
  async mounted() {
    await this.$store.dispatch('fetchData')

    const data = {
        labels: this.listNames,
        datasets: [{
        label: 'Completed',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgb(54, 162, 235)',
        borderWidth: 4,
        data: this.toggleTrue,
        },
        {
        label: 'Not completed',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgb(255, 99, 132)',
        borderWidth: 4,
        data: this.toggleFalse,
        }
    ]}
    const config = {
            type: 'bar',
            data: data,
            options: {
                responsive: true,  
                maintainAspectRatio: true,            
                scales: {
                    x: {
                        stacked: true,
                    },
                    y: {
                        stacked: true,
                        beginAtZero: true
                    }
                }
            }
        };
    const myChart = new Chart(document.getElementById('stackedBar'), config);
    myChart
  }
}
</script>