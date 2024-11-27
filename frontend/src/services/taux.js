import axios from 'axios';

const API_URL = 'http://localhost:8000';

export default {

  getTauxReco() {
    return axios.get(`${API_URL}/taux`);
  },

  getQuestion(){
    return axios.get(`${API_URL}/get_data`);
  },

  getTauxRecoIncrementations(incrementations, questions, marques) {
    return axios.get(`${API_URL}/taux/${incrementations}/${questions}/${marques}`);
  },

  get_bouton_I(questions, marque, start, stop, step){
    return axios.get(`${API_URL}/taux_bouton_I/${questions}/${marque}/${start}/${stop}/${step}`)
  },
  get_bouton_I_liee(questions, marque, start, stop, step){
    return axios.get(`${API_URL}/taux_bouton_I_liee/${questions}/${marque}/${start}/${stop}/${step}`)
  }
};
