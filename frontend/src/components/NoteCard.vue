<template>
	<div class="note-card" @click="emit('open', note.id)">
		<span class="note-card-title">{{ note.title }}</span>
		<span>{{ truncated }}</span>
		<span>{{ onlyDateAndHour }}</span>

		<button class="note-card-fav" @click.stop="emit('toggle-favourite', note.id)">
			{{ note.isFavourite ? "★" : "☆" }}
		</button>

		<button class="note-card-delete" @click.stop="emit('delete', note.id)">✖</button>
	</div>
</template>

<script setup lang="ts">
	import { computed } from "vue";

	type Note = {
		id: number;
		title: string;
		content: string;
		createdAt: string;
		isFavourite: boolean;
	};

	const props = withDefaults(
		defineProps<{
			note: Note;
			maxLength?: number;
		}>(),
		{
			maxLength: 10,
		}
	);

	const emit = defineEmits<{
		(e: "open", id: number): void;
		(e: "toggle-favourite", id: number): void;
		(e: "delete", id: number): void;
	}>();

	const onlyDateAndHour = computed(() => {
		return (
			props.note.createdAt.split("T")[0] +
			" " +
			props.note.createdAt.split("T")[1].split(":")[0] +
			":" +
			props.note.createdAt.split("T")[1].split(":")[1]
		);
	});

	const truncated = computed(() => {
		const c = props.note.content ?? "";
		return c.length > props.maxLength ? c.slice(0, props.maxLength) + "..." : c;
	});
</script>
