<template>
  <div v-if="loading" class="loading-popup">Loading...</div>
  <div class="header">
    <img src="../assets/logoApA.png" alt="Logo" class="logo" />
  </div>
  <div class="container-fluid">
    <table
      class="table table-bordered table-responsive-xl table-light table align-middle"
    >
      <thead>
        <tr>
          <th></th>
          <th v-for="marque in tauxRecoData" :key="marque.Brand">
            {{ marque.marque }}
            <div>
              <button @click="openPopup(marque)">I</button>
              <CustomPopup
                :isVisible="showPopup"
                @update:isVisible="showPopup = $event"
              >
                <template v-slot:default>
                  <div>
                    <div class="parent">
                      <h2>
                        Choice of Questions for {{ activeMarque?.marque }} Brand.
                      </h2>
                    </div>
                    <div>
                      <div>
                        <input
                          type="number"
                          v-model="start"
                          placeholder="Start"
                        />
                        <input
                          type="number"
                          v-model="stop"
                          placeholder="Stop"
                        />
                        <input
                          type="number"
                          v-model="step"
                          placeholder="Step"
                          step="0.1"
                        />
                      </div>
                      <p></p>
                      <input
                        type="checkbox"
                        id="select-all-questions"
                        v-model="selectAllQuestions"
                        @change="toggleSelectAllQuestions"
                      />
                      <label for="select-all-questions"
                        >Select all</label
                      >
                    </div>
                    <ul>
                      <div v-for="question in questions" :key="question.id">
                        <input
                          type="checkbox"
                          :id="`question-${question.id}`"
                          v-model="question.selected"
                        />
                        <label :for="`question-${question.id}`">{{
                          question.texte
                        }}</label>
                        {{ question.Noms }}
                      </div>
                    </ul>
                    <div>
                      <input
                        type="checkbox"
                        id="toggleRoute"
                        v-model="isCheckboxChecked"
                      />
                      <label for="toggleRoute">Combined Evolution ?</label>
                    </div>
                    <!-- <p>Ou</p>
                    <div>
                      <input
                        type="checkbox"
                        id="toggleRoute2"
                        v-model="isCheckboxChecked2"
                      />
                      <label for="toggleRoute">Évolution Combinée 2 à 2</label>
                    </div> -->
                    <button @click="submitQuestions">Submit</button>
                    <button @click="close" type="button" class="button-close">
                      Close
                    </button>
                  </div>
                </template>
              </CustomPopup>
              <CustomResponsePopup
                :isVisible="showResponsePopup"
                :responseData="responseData"
                :questions="questions"
                :activeMarque="activeMarque"
                @update:isVisible="onResponsePopupClosed"
              />
            </div>
          </th>
        </tr>
      </thead>
      <tbody class="table-group-divider">
        <tr v-for="question in questions" :key="question.Question">
          <td>
            {{ question.Question }} {{ question.Noms }}
            <div>
              <!-- <button @click="openPopup2(question)">Ouvrir la pop-up</button> -->
              <CustomPopup2
                :isVisible="showPopup2"
                @update:isVisible="showPopup2 = $event"
              >
                <template v-slot:default>
                  <div>
                    <h2>
                      Choix des Marques pour la question "{{
                        activeQuestion?.Noms
                      }}"
                    </h2>
                    <ul>
                      <div v-for="marque in tauxRecoData" :key="marque.Brand">
                        <input
                          type="checkbox"
                          :id="`Brand-${marque.Brand}`"
                          v-model="marque.selected2"
                        />
                        <label :for="`Brand-${marque.Brand}`">{{
                          marque.texte
                        }}</label>
                        {{ marque.marque }}
                      </div>
                    </ul>
                    <button @click="submitMarques">Soumettre</button>
                  </div>
                </template>
              </CustomPopup2>
            </div>
          </td>
          <td
            v-for="marque in tauxRecoData"
            :key="`${question.Question}-${marque.Brand}`"
          >
            <input
              type="number"
              :name="`input_${question.Question}_${marque.Brand}`"
              v-model="
                inputValues[`input_${question.Question}_${marque.Brand}`]
              "
              step="0.1"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <div>
    <table>
      <thead>
        <tr>
          <th>Brand</th>
          <th>KPI /1000</th>
          <th>New KPI /1000</th>
          <th>Evolution</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in sortedTauxRecoData" :key="item.Brand">
          <td>{{ item.marque }}</td>
          <td>{{ item.taux_reco }}</td>
          <td>{{ item.taux_reco_new }}</td>
          <td>{{ item.evolution }}</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="parent">
    <div>
      <table>
        <thead>
          <tr>
            <th>Brand Ranking</th>
            <th>% 1st</th>
            <th>% 2nd</th>
            <th>% 3rd</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in sortedTauxRecoData" :key="item.Brand">
            <td>{{ item.marque }}</td>
            <td>{{ item.pourcentage_1er }} %</td>
            <td>{{ item.pourcentage_2eme }} %</td>
            <td>{{ item.pourcentage_3eme }} %</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div>
      <table>
        <thead>
          <tr>
            <th>Brand Ranking New</th>
            <th>% 1st</th>
            <th>% 2nd</th>
            <th>% 3rd</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in sortedTauxRecoData" :key="item.Brand">
            <td>{{ item.marque }}</td>
            <td>{{ item.pourcentage_1er_new }} %</td>
            <td>{{ item.pourcentage_2eme_new }} %</td>
            <td>{{ item.pourcentage_3eme_new }} %</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div><button @click="sendData">Submit</button></div>

<div><button @click="resetData">Reset</button></div>
</template>

<script>
import TauxReco from "../services/taux";
import CustomPopup from "./Popup.vue";
import CustomPopup2 from "./Popup2.vue";
import CustomResponsePopup from "./CustomResponsePopup.vue";

export default {
  components: {
    CustomPopup,
    CustomPopup2,
    CustomResponsePopup,
  },
  data() {
    return {
      tauxRecoData: [],
      questions: [],
      inputValues: {},
      loading: false,
      showPopup: false,
      activeMarque: null,
      showPopup2: false,
      activeQuestion: null,
      selectAllMarques: false,
      selectAllQuestions: false,
      showResponsePopup: false,
      responseData: null,
      start: null,
      stop: null,
      step: null,
      isCheckboxChecked: false,
    };
  },
  computed: {
    sortedTauxRecoData() {
      return this.tauxRecoData.slice().sort((a, b) => a.Brand - b.Brand);
    },
  },
  watch: {},
  methods: {
    close() {
      this.showPopup = false;

      this.step = null;
      this.start = null;
      this.stop = null;

      this.selectAllQuestions = false;
      this.questions.forEach((question) => {
        question.selected = false;
      });

      this.activeMarque = null;

      this.isCheckboxChecked = false;
    },
    onResponsePopupClosed(isVisible) {
      this.showResponsePopup = isVisible;
      if (!isVisible) {
        this.showPopup = false;

        this.step = null;
        this.start = null;
        this.stop = null;

        this.selectAllQuestions = false;
        this.questions.forEach((question) => {
          question.selected = false;
        });

        this.activeMarque = null;

        this.isCheckboxChecked = false;
      }
    },
    fetchTauxReco() {
      this.loading = true;
      TauxReco.getTauxReco()
        .then((response) => {
          this.tauxRecoData = response.data;
          console.log(this.tauxRecoData)
        })
        .catch((error) => {
          console.error("Erreur lors de la récupération des données:", error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    resetData() {
      this.tauxRecoData.forEach((marque) => {
        marque.taux_reco_new = marque.taux_reco;
        marque.evolution = 0;
        marque.pourcentage_1er_new = marque.pourcentage_1er;
        marque.pourcentage_2eme_new = marque.pourcentage_2eme;
        marque.pourcentage_3eme_new = marque.pourcentage_3eme;
      });
      this.initializeInputValues();
    },
    fetchQuestion() {
      TauxReco.getQuestion().then((response) => {
        this.questions = response.data;
      });
    },
    initializeInputValues() {
      this.inputValues = {};
      for (let question of this.questions) {
        for (let marque of this.tauxRecoData) {
          this.inputValues[`input_${question.Question}_${marque.Brand}`] = "";
        }
      }
    },
    sendData() {
      this.loading = true;
      let incrementations = [];
      let questionsList = [];
      let marquesList = [];
      for (let question of this.questions) {
        for (let marque of this.tauxRecoData) {
          let inputName = `input_${question.Question}_${marque.Brand}`;
          let valeur = document.getElementsByName(inputName)[0].value;
          if (valeur) {
            incrementations.push(parseFloat(valeur));
            questionsList.push(question.Question);
            marquesList.push(marque.Brand);
          }
        }
      }
      TauxReco.getTauxRecoIncrementations(
        incrementations.join(","),
        questionsList.join(","),
        marquesList.join(",")
      )
        .then((response) => {
          response.data.forEach((item) => {
            item.resultat.forEach((res) => {
              const correspondingItem = this.tauxRecoData.find(
                (marque) => marque.Brand === res.Brand
              );
              console.log(this.tauxRecoData)
              if (correspondingItem) {
                correspondingItem.evolution = res.evolution;
                correspondingItem.taux_reco_new = res.taux_reco_new;
                
                correspondingItem.pourcentage_1er_new = res.pourcentage_1er_new;
                correspondingItem.pourcentage_2eme_new = res.pourcentage_2eme_new;
                correspondingItem.pourcentage_3eme_new = res.pourcentage_3eme_new;
              }
            });
          });
        })
        .catch((error) => {
          console.error("Erreur lors de l'envoi des données:", error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    fetchForBoutonI() {
      TauxReco.getQuestion().then((response) => {
        this.questions = response.data.map((question) => ({
          ...question,
          selected: false,
          selected2: false,
        }));
      });
    },
    submitQuestions() {
      let selectedQuestions;
      if (this.selectAllQuestions) {
        selectedQuestions = this.questions.map((q) => q.Question);
      } else {
        selectedQuestions = this.questions
          .filter((q) => q.selected)
          .map((q) => q.Question);
      }
      if (this.stop === null || this.start === null || this.step === null) {
        alert("Les champs Start Stop et Step doivent être remplie.");
        return;
      }
      if (selectedQuestions.length === 0) {
        alert("Aucune question sélectionnée.");
        return;
      }
      if (this.stop <= this.start) {
        alert("La valeur de 'stop' doit être supérieure à 'start'.");
        return;
      }
      if (this.step < 0) {
        alert("La valeur de 'step' doit être supérieure à 0.");
        return;
      }
      this.loading = true;
      if (!this.isCheckboxChecked) {
        TauxReco.get_bouton_I(
          selectedQuestions.join(","),
          this.activeMarque.Brand,
          this.start,
          this.stop,
          this.step
        )
          .then((response) => {
            this.showResponsePopup = true;
            this.responseData = response.data;
          })
          .catch((error) => {
            console.error("Erreur lors de l'envoi des données:", error);
          })
          .finally(() => {
            this.loading = false;
          });
      } else {
        TauxReco.get_bouton_I_liee(
          selectedQuestions.join(","),
          this.activeMarque.Brand,
          this.start,
          this.stop,
          this.step
        )
          .then((response) => {
            this.showResponsePopup = true;
            this.responseData = response.data;
          })
          .catch((error) => {
            console.error("Erreur lors de l'envoi des données:", error);
          })
          .finally(() => {
            this.loading = false;
          });
      }
    },
    openPopup(marque) {
      this.activeMarque = marque;
      this.showPopup = true;
    },
    openPopup2(question) {
      this.activeQuestion = question;
      this.showPopup2 = true;
    },
    toggleSelectAllQuestions() {
      if (this.selectAllQuestions) {
        this.questions.forEach((question) => {
          question.selected = true;
        });
      } else {
        this.questions.forEach((question) => {
          question.selected = false;
        });
      }
    },
    toggleSelectAllMarques() {
      this.selectAllMarques = !this.selectAllMarques;
      this.questions.forEach((question) => {
        question.selected = this.selectAllQuestions;
      });
    },
  },

  created() {
    this.fetchTauxReco();
    this.fetchQuestion();
  },
};
</script>

<style>
.close-icon {
  font-size: 14px;
  font-weight: bold;
}
.parent {
display: grid;
grid-template-columns: repeat(2, 1fr);
grid-template-rows: 1fr;
grid-column-gap: 0px;
grid-row-gap: 0px;
}
.close-button {
  position: static;
  cursor: pointer;
  width: 20px;
  height: 20px;
  background-color: red;
  display: flex;
  justify-content: center;
  align-items: center;
}
button,
input {
  cursor: pointer;
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

.loading-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  z-index: 1000;
}
.logo {
  height: 50px;
  margin-left: 50px;
}
.header {
  width: 100%;
  padding: 10px 0;
  position: relative;
  display: flex;
  align-items: center;
}
</style>
