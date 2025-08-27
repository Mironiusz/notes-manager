<template>
	<div class="dashboard">
		<h2 class="dashboard-title">Wszystkie notatki</h2>
		<button class="dashboard-create" @click="createNote">Nowa notatka</button>

		<div class="dashboard-content">
			<NoteCard
				v-for="n in notes"
				:key="n.id"
				:note="n"
				:maxLength="50"
				@open="openNote"
				@toggle-favourite="switchFavourite"
				@delete="deleteNote" />
		</div>
	</div>
</template>

<script setup lang="ts">
	import { ref } from "vue";
	import { useRouter } from "vue-router";
	import axios from "axios";
	import NoteCard from "../components/NoteCard.vue";

	type Note = {
		id: number;
		title: string;
		content: string;
		createdAt: string;
		isFavourite: boolean;
	};

	const router = useRouter();
	const notes = ref<Note[]>([]);

	const api = axios.create({
		baseURL: "http://localhost:8000/api/v1/notes",
	});

	async function loadNotes() {
		try {
			const res = await api.get<Note[]>("/", {});
			notes.value = res.data;
		} catch (e) {
			console.error(e);
		}
	}

	function openNote(id: number) {
		router.push({ path: `/note/${id}` });
	}

	async function deleteNote(id: number) {
		if (!confirm("Na pewno usunąć tę notatkę?")) return;
		try {
			await api.delete(`/${id}`);
			notes.value = notes.value.filter((n) => n.id !== id);
		} catch (err) {
			console.error("Błąd przy usuwaniu notatki:", err);
		}
	}

	async function switchFavourite(id: number) {
		try {
			const n = notes.value.find((n) => n.id === id);
			if (!n) return;
			const res = await api.patch<Note>(`/${id}`, { isFavourite: !n.isFavourite });
			n.isFavourite = res.data.isFavourite;
		} catch (err) {
			console.error("Błąd przy zmianie ulubionej notatki:", err);
		}
	}

	async function createNote() {
		const newNote = {
			title: "Nowa notatka",
			content: "Treść notatki",
			isFavourite: false,
		};
		const res = await api.post<Note>("/", newNote);
		router.push({ path: `/note/${res.data.id}` });
	}

	loadNotes();
</script>
