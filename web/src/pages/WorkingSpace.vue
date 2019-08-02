<template>
  <div class="annotator">
    <div class="annotator-main">
      <ElCard class="box-card" v-if="sentence">{{ sentence.text}}</ElCard>
      <KeyBoardSettings :annotations="annotations" @update="updateAnnotation" @onBlur="setKeyboard"></KeyBoardSettings>
    </div>
    <div class="button-group">
      <div class="annotator-button-group">
        <Tag
          v-for="annotation in annotations"
          :key="annotation.name"
          :size="tagSize"
          :name="annotation.name"
          :shortcuts="annotation.key"
          :selected="sentence && sentence.annotation_id === annotation.id"
          :machine-selected=" sentence && sentence.machine_annotation_id === annotation.id"
          @selectTag="handleSelectTag(annotation.id)"
        ></Tag>
      </div>
      <ElButtonGroup class="action-button-group">
        <ElButton type="primary" icon="el-icon-caret-left" @click="handlePrev">上一个[左键]</ElButton>
        <ElButton type="info" icon="el-icon-close" @click="handleSkip">忽略[空格键]</ElButton>
        <ElButton type="primary" icon="el-icon-caret-right" @click="handleNext">下一个[右键]</ElButton>
      </ElButtonGroup>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import apis from '@/api'

import Tag from '@/components/Tag.vue'
import KeyBoardSettings from '@/components/KeyBoardSettings.vue'

export default {
  name: 'working-space',
  components: {
    Tag,
    KeyBoardSettings
  },
  data() {
    return {
      sentences: [],
      sentenceIndex: 0
    }
  },
  watch: {
    dataSource(nextDataSource) {
      this.sentences = nextDataSource.data
      this.sentenceIndex = 0
    }
  },
  computed: {
    ...mapState({
      annotations: state => state.annotations,
      dataSource: state => state.dataSource
    }),
    tagSize() {
      return this.annotations.length > 5 ? 'small' : 'large'
    },
    sentence() {
      return this.sentences ? this.sentences[this.sentenceIndex] : null
    }
  },
  async created() {
    const { data, total_count } = await apis.getUnlabeledAnnotationList().then(resp => {
      return JSON.parse(resp.data.data)
    })
    this.$store.commit('updateDataSource', { data, count: total_count })
    await this.updateProgress()
    await this.updateHistory()
    this.setKeyboard()
  },
  beforeDestroy() {
    document.removeEventListener('keydown', this.handleKeyDown)
  },
  methods: {
    async handleSelectTag(annotationId) {
      this.$set(this.sentence, 'annotation_id', annotationId)
      await apis.annotateText(this.sentence.text, this.sentence.annotation_id, this.sentence.uuid)
      await this.updateProgress()
      await this.updateHistory()
    },
    handleKeyDown(event) {
      const key = event.keyCode
      const annotationKeyBoard = {}
      for (const annotation of this.annotations) {
        if (annotation['keyCode']) {
          annotationKeyBoard[annotation['keyCode']] = annotation.id
        }
      }
      switch (key) {
        case 37:
          this.handlePrev()
          break
        case 39:
          this.handleNext()
          break
        case 32:
          this.handleSkip()
          break
        default:
          const id = annotationKeyBoard[key]
          if (id) {
            this.sentence.annotation_id = id
          }
          break
      }
    },
    setKeyboard() {
      document.removeEventListener('keydown', this.handleKeyDown)
      document.addEventListener('keydown', this.handleKeyDown)
    },
    updateAnnotation(index, annotation) {
      this.annotations.map((tempAnnotation, idx) => {
        if (annotation.keyCode === tempAnnotation.keyCode) {
          this.annotations.splice(idx, 1, {
            id: tempAnnotation.id,
            name: tempAnnotation.name
          })
        }
      })

      this.annotations.splice(index, 1, annotation)
    },
    handlePrev() {
      if (!this.sentence || this.sentenceIndex < 1) {
        return
      }
      this.sentenceIndex--
    },
    async handleSkip() {
      if (!this.sentence || this.sentence.id === this.sentences.length - 1) {
        return
      }
      this.sentence.annotation_id = null
      this.sentenceIndex++
      await this.updateProgress()
    },
    handleNext() {
      if (!this.sentence || this.sentenceIndex === this.sentences.length - 1) {
        return
      }
      this.sentenceIndex++
    },
    async updateProgress() {
      if (this.sentences.length > 0) {
        const done = this.sentences.filter(
          s => s.annotation_id !== undefined && s.annotation_id !== null
        ).length
        this.$store.commit('updateProgress', {
          done: done,
          count: this.sentences.length
        })
      }
    },
    async updateHistory() {
      const {
        data: { data }
      } = await apis.getAnnotationHistory()
      this.$store.commit('updateHistory', JSON.parse(data))
    }
  }
}
</script>

<style lang="scss" scoped>
.annotator {
  height: 100vh;
  display: flex;
  flex-direction: column;
  flex: 1;
  cursor: pointer;
  background: white;
  color: #333;

  .annotator-main {
    flex: 1;
    display: flex;
    margin: 20px 20px 0 20px;

    .box-card {
      flex: 1;
      margin-right: 20px;
      font-size: 24px;
      text-align: left;
      overflow-y: auto;
    }
  }

  .button-group {
    margin: auto;
    text-align: center;

    > div {
      width: 100%;
      display: flex;
      padding: 20px;
    }

    .annotator-button-group {
      justify-content: space-around;
    }

    .action-button-group {
      justify-content: center;
    }
  }
}
</style>
