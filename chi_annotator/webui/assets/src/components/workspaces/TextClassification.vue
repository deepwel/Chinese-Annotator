<template>
  <div class="annotator">
    <el-card class="box-card">
      {{ sentence.content }}
    </el-card>
    <div class="button-group">
      <div class="annotator-button-group">
        <tag
          v-for="annotation in annotations"
          :key="annotation.id"
          :size="tagSize"
          :name="annotation.name"
          :shortcuts="annotation.id + 1 + ''"
          :selected="sentence.annotation_id === annotation.id"
          :machine-selected="sentence.machine_annotation_id === annotation.id"
          @selectTag="selectTag(annotation.id)"
        ></tag>
      </div>
      <div class="action-button-group">
        <action-button name="上一个(左键)" icon="el-icon-caret-left" @onClick="prev"></action-button>
        <action-button name="忽略(X键)" icon="el-icon-close" @onClick="neglect"></action-button>
        <action-button name="下一个(右键)" icon="el-icon-caret-right" @onClick="next"></action-button>
      </div>
    </div>
  </div>
</template>

<script>
  import Tag from '../Tag'
  import Button from '../Button'
  import mockData from '../../../mock'

  export default {
    name: 'text-classification',
    data: function () {
      return {
        sentence: null,
        sentences: [],
        annotations: []
      }
    },
    components: {
      'tag': Tag,
      'action-button': Button
    },
    computed: {
      tagSize: function () {
        return this.annotations.length > 5 ? 'small' : 'large'
      }
    },
    methods: {
      selectTag: function (selectedId) {
        this.sentence.annotation_id = selectedId
      },
      prev: function () {
        this.updateProgress()

        if (!this.sentence || this.sentence.id < 1) {
          return
        }

        this.sentence = this.sentences[this.sentence.id - 1]
      },
      neglect: function () {
        this.sentence.annotation_id = false
        this.updateProgress()

        if (!this.sentence || this.sentence.id === this.sentences.length - 1) {
          return
        }

        this.sentence = this.sentences[this.sentence.id + 1]
      },
      next: function () {
        this.updateProgress()

        if (!this.sentence || this.sentence.id === this.sentences.length - 1) {
          return
        }

        this.sentence = this.sentences[this.sentence.id + 1]
      },
      updateProgress: function () {
        if (this.sentences.length > 0) {
          let done = 0

          for (let sentence of this.sentences) {
            if (sentence.annotation_id !== null) {
              done++
            }
          }

          this.$store.commit('updateProgress', {
            done: done,
            count: this.sentences.length
          })
        }
      }
    },
    created: function () {
      new Promise((resolve, reject) => {
        const sentences = mockData.data.sentences
        let component = this

        for (const sentence of sentences) {
          if (!sentence.annotation_id) {
            this.sentence = sentence
            break
          }
        }

        this.sentences = sentences
        this.annotations = mockData.data.annotations
        this.$store.commit('updateBasic', mockData.data.basic)
        this.updateProgress()

        document.onkeydown = function () {
          let key = window.event.keyCode

          switch (key) {
            case 37:
              component.prev()
              break
            case 39:
              component.next()
              break
            case 88:
              component.neglect()
              break
            default:
              const number = key - 48

              if (number > 0 && number < component.annotations.length + 1) {
                component.sentence.annotation_id = number - 1
              }
              break
          }
        }
      }).catch(err => {
        console.log(err)
      })
    }
  }
</script>

<style>
  .annotator{
    height: 100vh;
    display: flex;
    flex-direction: column;
    flex: 1;
    cursor: pointer;
    background: white;
    color: #333;
  }

  .annotator .box-card {
    margin: 20px 20px 0 20px;
    flex: 1;
    font-size: 24px;
    text-align: left;
    overflow-y: auto;
  }

  .annotator .button-group {
    width: 100%;
  }

  .annotator .button-group > div {
    width: 100%;
    display: flex;
    padding: 20px;
  }

  .annotator .button-group .annotator-button-group {
    justify-content: space-around;
  }

  .annotator .button-group .action-button-group {
    padding-top: 0;
    justify-content: space-between;
  }
</style>
