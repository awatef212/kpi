<template>
  <div v-if="isVisible" class="response-popup">
    <div class="response-content">
      <h2>Results for {{ activeMarque?.marque }}</h2>
      <div>{{ getCurrentDateTime() }}</div>

      <!-- Boutons pour changer de vue -->
      <button v-if="currentView === 'table'" @click="showGraphView">
        Switch Vue
      </button>
      <button v-if="currentView === 'graph'" @click="showTableView">
        Switch Vue
      </button>
      <button @click="closePopup">Close</button>

      <!-- Boutons de téléchargement, affichés seulement dans la vue tableau -->
      <div v-if="currentView === 'table'">
        <button @click="triggerDownload">Excel</button>
        <button @click="downloadTableAsPNG">Image</button>
      </div>

      <!-- Vue Tableau -->
      <div v-if="currentView === 'table'">
        <table ref="pdfTable" v-if="responseData.length > 0">
          <table ref="pdfTable" v-if="responseData.length > 0">
            <thead>
              <tr>
                <th>Question(s)</th>
                <th>Increment</th>
                <th>New KPI /1000</th>
                <th>Evolution</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="items in responseData" :key="items[0].Brand">
                <td>{{ getQuestionName(items[0].question) }}</td>
                <td>{{ items[0].incrementation }}</td>
                <td>{{ items[0].taux_reco_new }}</td>
                <td>{{ items[0].evolution }}</td>
              </tr>
            </tbody>
          </table>
          <div v-else>
            <p>Aucune donnée à afficher.</p>
          </div>
        </table>
        <div v-else>
          <p>Aucune donnée à afficher.</p>
        </div>
      </div>

      <!-- Vue Graphique -->
      <div v-else-if="currentView === 'graph'" class="graph-view">
        <button @click="downloadGraphAsPNG">Image</button>
        <div>
          <table>
            <thead>
              <tr>
                <th>Question</th>
                <th>Low KPI Average</th>
                <th>High KPI Average</th>
                <th>Classification</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in tableData" :key="item.question">
                <td>{{ item.question }}</td>
                <td>{{ item.lowKPIAverage }}</td>
                <td>{{ item.highKPIAverage }}</td>
                <td>{{ item.Golden }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="canvas-container">
          <canvas ref="canvas"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import html2canvas from "html2canvas";
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
  data() {
    return {
      currentView: "table",
      xAxisStart: 0,
      xAxisEnd: 100,
      chartInstance: null,
    };
  },
  props: {
    questions: Array,
    activeMarque: Object,
    isVisible: {
      type: Boolean,
      required: true,
    },

    responseData: {
      type: Array,
      default: () => [],
    },
  },
  mounted() {},
  methods: {
    closePopup() {
      this.chartInstance = null;
      this.currentView = "table";
      this.xAxisStart = 0;
      this.xAxisEnd = 100;
      this.$emit("update:isVisible", false);
    },
    getQuestionName(questionId) {
      if (!questionId) {
        return "Question non spécifiée";
      }
      if (questionId.includes(",")) {
        const ids = questionId.split(",");
        const names = ids.map((id) => {
          const question = this.questions.find(
            (q) => q.Question.toString() === id.trim()
          );
          return question ? question.Noms : "Inconnu";
        });
        return names.join(", ");
      } else {
        const question = this.questions.find(
          (q) => q.Question.toString() === questionId
        );
        return question ? question.Noms : "Inconnu";
      }
    },
    getCurrentDateTime() {
      const current = new Date();
      const date = `${this.padToTwoDigits(
        current.getDate()
      )}/${this.padToTwoDigits(
        current.getMonth() + 1
      )}/${current.getFullYear()} ${this.padToTwoDigits(
        current.getHours()
      )}H${this.padToTwoDigits(current.getMinutes())}`;
      return date;
    },
    padToTwoDigits(number) {
      return number.toString().padStart(2, "0");
    },
    convertToCSV(data) {
      const csvRows = [];

      const headers = [
        "Question(s)",
        "Incrémentation",
        "Taux Reco Nouveau",
        "Évolution",
      ];
      csvRows.push(headers.join(","));

      for (const row of data) {
        const values = [
          this.getQuestionName(row[0].question),
          row[0].incrementation,
          row[0].taux_reco_new,
          row[0].evolution,
        ];

        const escapedValues = values.map((value) => {
          const escaped = ("" + value).replace(/"/g, '\\"');
          return `"${escaped}"`;
        });

        csvRows.push(escapedValues.join(","));
      }

      return csvRows.join("\n");
    },
    downloadCSV(data, filename) {
      const blob = new Blob([data], { type: "text/csv" });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.setAttribute("hidden", "");
      a.setAttribute("href", url);
      a.setAttribute("download", filename);
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    },
    triggerDownload() {
      const csvData = this.convertToCSV(this.responseData);
      const name_file =
        this.activeMarque.marque + "_" + this.getCurrentDateTime();
      this.downloadCSV(csvData, name_file);
    },
    downloadTableAsPNG() {
      const element = this.$refs.pdfTable;

      html2canvas(element).then((canvas) => {
        const image = canvas.toDataURL("image/png", 1.0);
        const link = document.createElement("a");
        link.href = image;
        link.download =
          this.activeMarque.marque +
          "_" +
          this.getCurrentDateTime() +
          "_Tableau.png";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      });
    },
    downloadGraphAsPNG() {
      const element = this.$refs.canvas;
      html2canvas(element).then((canvas) => {
        const image = canvas.toDataURL("image/png", 1.0);
        const link = document.createElement("a");
        link.href = image;
        link.download =
          this.activeMarque.marque +
          "_" +
          this.getCurrentDateTime() +
          "_Graph.png";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      });
    },
    showTableView() {
      this.currentView = "table";
    },
    showGraphView() {
      this.currentView = "graph";
      this.$nextTick(() => {
        if (this.chart) {
          this.chart.destroy();
        }
        this.createChart();
      });
    },
    prepareChartData(responseData) {
      const dataPerQuestion = {};

      responseData.forEach((items) => {
        const question = items[0].question;
        if (!dataPerQuestion[question]) {
          dataPerQuestion[question] = [];
        }
        dataPerQuestion[question].push({
          x: items[0].incrementation,
          y: items[0].taux_reco_new,
        });
      });

      const datasets = Object.keys(dataPerQuestion).map((question) => ({
        label: this.getQuestionName(question),
        data: dataPerQuestion[question],
        fill: false,
        borderColor: this.getRandomColor(),
      }));

      return {
        datasets: datasets,
      };
    },
    getRandomColor() {
      const r = Math.floor(Math.random() * 255);
      const g = Math.floor(Math.random() * 255);
      const b = Math.floor(Math.random() * 255);
      return `rgb(${r}, ${g}, ${b})`;
    },
    calculateMinMaxIncrement() {
      if (this.responseData.length === 0) {
        this.xAxisStart = 0;
        this.xAxisEnd = 100;
        return;
      }

      let minIncrement = this.responseData[0][0].incrementation;
      let maxIncrement = this.responseData[0][0].incrementation;

      for (const items of this.responseData) {
        const increment = items[0].incrementation;
        if (increment < minIncrement) {
          minIncrement = increment;
        }
        if (increment > maxIncrement) {
          maxIncrement = increment;
        }
      }

      this.xAxisStart = minIncrement;
      this.xAxisEnd = maxIncrement;
    },
    createChart() {
      if (this.chartInstance) {
        this.chartInstance.destroy();
      }
      this.calculateMinMaxIncrement();
      const chartData = this.prepareChartData(this.responseData);
      const ctx = this.$refs.canvas.getContext("2d");
      this.chartInstance = new Chart(ctx, {
        type: "line",
        data: chartData,
        options: {
          scales: {
            x: {
              type: "linear",
              position: "bottom",
            },
          },
        },
      });
    },
  },
  computed: {
    tableData() {
      let dataByQuestion = {};
      this.responseData.forEach((item) => {
        if (!dataByQuestion[item[0].question]) {
          dataByQuestion[item[0].question] = [];
        }
        dataByQuestion[item[0].question].push(item[0]);
      });
      let table = Object.keys(dataByQuestion).map((question) => {
        let items = dataByQuestion[question];
        items.sort((a, b) => a.incrementation - b.incrementation);
        let lowKPI =
          items.slice(0, 3).reduce((acc, curr) => acc + curr.taux_reco_new, 0) /
          3;
        let highKPI =
          items.slice(-3).reduce((acc, curr) => acc + curr.taux_reco_new, 0) /
          3;
        let currentKPI = items.find((item) => item.incrementation === 0);
        let currentKPIValue = currentKPI ? currentKPI.taux_reco_new : "N/A";
        return {
          question: this.getQuestionName(question),
          lowKPIAverage: lowKPI.toFixed(2),
          highKPIAverage: highKPI.toFixed(2),
          currentKPI_: currentKPIValue,
        };
      });

      
      let medianIndex = Math.floor(table.length / 2);
      let lowKPIMedian = parseFloat(table[medianIndex].lowKPIAverage);

      let highKPIMedian = parseFloat(table[medianIndex].highKPIAverage);

      table.forEach((item) => {
        if (
          parseFloat(item.lowKPIAverage) <= lowKPIMedian &&
          parseFloat(item.highKPIAverage) >= highKPIMedian
        ) {
          item.Golden = "Golden";
        } else if (
          parseFloat(item.lowKPIAverage) >= lowKPIMedian &&
          parseFloat(item.highKPIAverage) >= highKPIMedian
        ) {
          item.Golden = "Positive";
        } else if (
          parseFloat(item.lowKPIAverage) <= lowKPIMedian &&
          parseFloat(item.highKPIAverage) <= highKPIMedian
        ) {
          item.Golden = "Negative";
        } else {
          item.Golden = "Neutre";
        }
      });
      table.sort(
        (a, b) => parseFloat(b.highKPIAverage) - parseFloat(a.highKPIAverage)
      );
      return table;
    },
  },
};
</script>

<style>
.response-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.response-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  max-height: 90%;
  overflow-y: auto;
  width: 100%;
  height: 100%;
}
table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f4f4f4;
}

.graph-view {
  width: 100%;
  height: 100%;
}

.canvas-container {
  width: 90%;
  height: 90%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
