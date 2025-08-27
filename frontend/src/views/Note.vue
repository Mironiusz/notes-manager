<template>
	<div class="note" v-if="!loading">
		<div class="note-header">
			<input v-model="note.title" placeholder="Wpisz tytuł" />
			<span class="note-meta">{{ formatDate(note.createdAt) }}</span>
		</div>

		<div class="note-body">
			<textarea v-model="note.content" placeholder="Wpisz treść"></textarea>
		</div>

		<div class="note-actions">
			<button class="note-actions-save" @click="saveNote">✔</button>
			<button v-if="isExisting" class="note-actions-delete" @click="deleteNote">✖</button>
			<button class="note-actions-fav" @click="switchFavourite">
				{{ note.isFavourite ? "★" : "☆" }}
			</button>
		</div>
	</div>

	<div v-else>Ładowanie…</div>
</template>

<script setup lang="ts">
	import { ref, computed } from "vue";
	import { useRoute, useRouter } from "vue-router";
	import axios from "axios";

	type Note = {
		id?: number;
		title: string;
		content: string;
		createdAt: string;
		isFavourite: boolean;
	};

	const route = useRoute();
	const router = useRouter();

	const noteIdParam = route.params.id as string | undefined;
	const noteId = noteIdParam ? Number(noteIdParam) : NaN;
	const isExisting = computed(() => Number.isFinite(noteId));

	const API_BASE = "http://localhost:8000/api/v1/notes";
	const api = axios.create({ baseURL: API_BASE });

	const loading = ref(true);
	const note = ref<Note>({
		id: isExisting.value ? noteId : undefined,
		title: "",
		content: "",
		createdAt: new Date().toISOString(),
		isFavourite: false,
	});

	function formatDate(iso: string) {
		if (!iso) return "";
		try {
			const d = new Date(iso);
			return d.toLocaleString();
		} catch {
			return iso;
		}
	}

	async function loadNote() {
		if (!isExisting.value) {
			loading.value = false;
			return;
		}
		try {
			const res = await api.get<Note>(`/${noteId}`);
			note.value = res.data;
		} catch (e) {
			console.error("Nie udało się pobrać notatki:", e);
			router.replace("/");
		} finally {
			loading.value = false;
		}
	}

	async function saveNote() {
		try {
			if (!note.value.title.trim()) {
				alert("Tytuł jest wymagany");
				return;
			}

			if (isExisting.value) {
				const payload = {
					title: note.value.title,
					content: note.value.content,
					isFavourite: note.value.isFavourite,
				};
				const res = await api.patch<Note>(`/${noteId}`, payload);
				note.value = res.data;
				alert("Zapisano zmiany");
			} else {
				const payload = {
					title: note.value.title,
					content: note.value.content,
					isFavourite: note.value.isFavourite,
				};
				const res = await api.post<Note>("/", payload);
				note.value = res.data;
				router.replace(`/note/${res.data.id}`);
			}
		} catch (e) {
			console.error("Błąd zapisu notatki:", e);
			alert("Nie udało się zapisać notatki");
		}
	}

	async function deleteNote() {
		if (!isExisting.value || !note.value.id) return;
		if (!confirm("Na pewno usunąć tę notatkę?")) return;

		try {
			await api.delete(`/${note.value.id}`);
			router.replace("/");
		} catch (e) {
			console.error("Błąd usuwania notatki:", e);
			alert("Nie udało się usunąć notatki");
		}
	}

	async function switchFavourite() {
		await saveNote();
		try {
			note.value.isFavourite = !note.value.isFavourite;

			if (isExisting.value && note.value.id) {
				const res = await api.patch<Note>(`/${note.value.id}`, {
					isFavourite: note.value.isFavourite,
				});
				note.value = res.data;
			}
		} catch (e) {
			note.value.isFavourite = !note.value.isFavourite;
			console.error("Błąd przełączania ulubionej:", e);
		}
	}

	loadNote();
</script>
