<template>
    <div>
      <h1>Taux de Recommandation</h1>
      <table>
        <thead>
          <tr>
            <th>Marque</th>
            <th>Taux Reco</th>
            <th>Taux Reco Nouveau</th>
            <th>Évolution</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in tauxRecoData" :key="item.Brand">
            <td>{{ item.marque }}</td>
            <td>{{ item.taux_reco }}</td>
            <td>{{ item.taux_reco_new }}</td>
            <td>{{ item.evolution }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import api from '@/api'; 

  export default {
    data() {
      return {
        tauxRecoData: []
      };
    },
    methods: {
      fetchTauxReco() {
        api.getTauxReco()
          .then(response => {
            this.tauxRecoData = response.data;
          })
          .catch(error => {
            console.error("Erreur lors de la récupération des données:", error);
          });
      }
    },
    created() {
      this.fetchTauxReco();
    }
  };
  </script>
  
  <style>
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  
  th {
    background-color: #f4f4f4;
  }
  </style>
  