<template>
  <div class="container-fluid px-5">
    <div class="row mt-3 py-3">
      <div class="col-md-12">
        <h2>Control net / Replicate</h2>
      </div>
    </div>
    <div class="row">
      <div class="col-12 col-sm col-md-5 col-lg-4 py-2">
        <div class="row d-flex align-items-center">
          <div class="col">
            <label class="form-label card-text">Canvas</label>
          </div>
          <div class="col-auto">
            <i type="button" class="fa-solid fa-eraser fa-lg" @click="clearCanvas"></i>
          </div>
        </div>
        <div class="ratio ratio-1x1 mt-3">
          <canvas
            ref="myCanvas"
            class="shadow border border-dark-subtle bg-body-tertiary rounded w-100"
            id="myCanvas"
            @mousedown="startDrawing"
            @mousemove="drawLine"
            @mouseup="stopDrawing"
            @mouseout="stopDrawing"
            @contextmenu="preventContextMenu"
          >
          </canvas>
          <div v-if="loading" class="loading-overlay">
            <img src="../assets/loading.gif" class="rounded img-fluid" alt="Loading Animation">
          </div>
        </div>
        <form @submit.prevent="sendInput" class="mt-3">
          <div class="mb-3">
            <label for="prompt" class="form-label">Your prompt</label>
            <textarea type="text" class="form-control resizable-textarea" id="prompt" v-model="prompt" placeholder="..."></textarea>
          </div>
          <div class="row gx-2">
            <div class="col col-sm-12 col-xl">
              <label class="form-label">Number of samples</label>
              <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle w-100" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                  {{ numOfSamples }}
                </button>
                <ul class="dropdown-menu w-100 px-2">
                  <li @click="numOfSamples = 1">1</li>
                  <li @click="numOfSamples = 4">4</li>
                </ul>
              </div>
            </div>
            <div class="col col-sm-12 col-xl">
              <div class="dropdown">
                <label class="form-label">Resolution</label>
                <button class="btn btn-secondary dropdown-toggle w-100" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                  {{ resolution }}
                </button>
                <ul class="dropdown-menu w-100 px-2">
                  <li @click="resolution = 256">256</li>
                  <li @click="resolution = 512">512</li>
                  <li @click="resolution = 768">768</li>
                </ul>
              </div>
            </div>
          </div>
          <button type="submit" class="btn btn-primary mt-3">Submit</button>
        </form>
      </div>
      <div class="col-12 col-sm col-md-7 col-lg-8 py-2 px-sm-3 px-md-3 px-xl-5 mt-3 mt-sm-0">
        <div class="row">
          <div class="col-md-12">
            <label class="form-label">Output</label>
          </div>
        </div>
        <div class="row mt-2">
          <div class="col-md-12">
            <div v-if="output.length > 0" class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
              <div v-for="(image, index) in output" :key="index" class="col">
                <img :src="image" class="card-img-top img-fluid rounded-3" alt="...">
              </div>
            </div>
            <div v-else class="alert alert-info" role="alert">
              No output yet.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HomeView',
  components: {

  },
  mounted () {
    this.context = this.$refs.myCanvas.getContext("2d");
    this.setupCanvas()
  },
  data() {
    return {
      numOfSamples: 1,
      resolution: 512,
      prompt: '',
      image: null,
      output: [],
      isDrawing: false,
      mouse: {
        x: undefined,
        y: undefined
      },
      oldX: undefined,
      oldY: undefined,
      lineWidth: 5,
      backgroundColor: '#F8F9FA',
      loading: false,
      context: null
    }
  },
  methods: {
    setupCanvas() {
      const canvas = this.$refs.myCanvas;
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    },
    async sendInput() {
      this.loading = true

      const data = JSON.stringify({
        "image": this.getImageUrl(),
        "prompt": this.prompt,
        "num_samples": this.numOfSamples,
        "image_resolution": this.resolution
      })

      await axios
        .post('/api/v1/getImages/', data, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': 'csrftoken'
          }
        })
        .then(response => {
          console.log(response.data)
          this.output.push(...response.data)
        })
        .catch(error => {
          console.log(error)
        })
        .finally(() => {
          this.loading = false
        });
    },
    getImageUrl() {
      const canvas = this.$refs.myCanvas
      const dataURL = canvas.toDataURL("image/jpeg")

      return dataURL
    },
    startDrawing(e) {
      this.isDrawing = true;

      this.setMouseCoordinates(e);
      this.setStrokeStyle(e);

      this.oldX = this.mouse.x;
      this.oldY = this.mouse.y;

      this.draw();
    },

    drawLine(e) {
      if (!this.isDrawing) return;

      this.setMouseCoordinates(e);
      this.draw();

      this.oldX = this.mouse.x;
      this.oldY = this.mouse.y;
    },
    draw() {
      this.context.beginPath();
      this.context.moveTo(this.oldX, this.oldY);
      this.context.lineTo(this.mouse.x, this.mouse.y);
      this.context.stroke();
    },
    stopDrawing() {
      this.isDrawing = false;
      this.context.closePath();
    },
    clearCanvas() {
      const canvas = this.$refs.myCanvas;
      this.context.clearRect(0, 0, canvas.width, canvas.height);
    },
    setMouseCoordinates(e) {
      this.mouse.x = e.offsetX;
      this.mouse.y = e.offsetY;
    },
    setStrokeStyle(e) {
      if (e.button === 0) {
        this.context.strokeStyle = 'black';
        this.context.lineWidth = this.lineWidth;
      } else if (e.button === 2) {
        this.context.strokeStyle = this.backgroundColor;
        this.context.lineWidth = this.lineWidth * 5;
      }
    },
    preventContextMenu(e) {
      e.preventDefault();
    }
  }
}
</script>

<style scoped>
.resizable-textarea {
  resize: vertical;
  min-height: 100px;
  max-height: 300px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}
</style>
