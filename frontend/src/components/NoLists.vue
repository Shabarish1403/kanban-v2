<template>
    <div style="padding-top:250px">
        <h2>There are no lists on card</h2>
        <b-button variant="primary" v-b-modal.addList>
            <b-icon icon="plus-circle"></b-icon><br>
            Add List
        </b-button>
    </div>
</template>

<script>
export default {
    name: 'NoLists',
}
</script>

<style scoped>
</style>