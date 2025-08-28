<template>
	<div class="dashboard">
		<div class="dashboard-header">
			<h2 class="dashboard-title">Wszystkie notatki</h2>

			<div class="dashboard-filters">
				<input
					class="filter-input"
					v-model="searchQuery"
					@input="onSearchInput"
					type="search"
					placeholder="Szukaj w tytułach…" />

				<label class="filter-check">
					<input type="checkbox" v-model="favouriteOnly" @change="loadNotes" />
					<span>Tylko ulubione</span>
				</label>

				<select class="filter-select" v-model="sort" @change="loadNotes">
					<option value="created_desc">Najnowsze (utworzenie)</option>
					<option value="created_asc">Najstarsze (utworzenie)</option>
					<option value="updated_desc">Najnowsze (aktualizacja)</option>
					<option value="updated_asc">Najstarsze (aktualizacja)</option>
				</select>

				<button class="dashboard-create" @click="createNote">Nowa notatka</button>
			</div>
		</div>

		<div class="dashboard-content">
			<template v-if="favNotes.length">
				<div class="group-header">Ulubione</div>
				<NoteCard
					v-for="n in favNotes"
					:key="n.id"
					:note="n"
					:maxLength="50"
					@open="openNote"
					@toggle-favourite="switchFavourite"
					@delete="deleteNote" />
			</template>

			<template v-if="otherNotes.length">
				<div class="group-header" v-if="!favouriteOnly && favNotes.length">Pozostałe</div>
				<NoteCard
					v-for="n in otherNotes"
					:key="n.id"
					:note="n"
					:maxLength="50"
					@open="openNote"
					@toggle-favourite="switchFavourite"
					@delete="deleteNote" />
			</template>

			<div v-if="!favNotes.length && !otherNotes.length" class="empty">Brak notatek spełniających kryteria.</div>
		</div>
	</div>
</template>

<script setup lang="ts">
	import { ref, computed } from "vue";
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

	const sort = ref<"created_desc" | "created_asc" | "updated_desc" | "updated_asc">("created_desc");
	const favouriteOnly = ref<boolean>(false);
	const searchQuery = ref<string>("");

	async function loadNotes() {
		try {
			const params: Record<string, any> = {
				sort: sort.value,
				page: 1,
				page_size: 200,
			};
			if (favouriteOnly.value) params.favourite = true;
			if (searchQuery.value.trim()) params.query = searchQuery.value.trim();

			const res = await api.get<Note[]>("/", { params });
			notes.value = res.data;
		} catch (e) {
			console.error(e);
		}
	}

	let t: number | undefined;
	function onSearchInput() {
		if (t) window.clearTimeout(t);
		t = window.setTimeout(() => {
			loadNotes();
		}, 300);
	}

	function openNote(id: number) {
		router.push({ path: `/note/${id}` });
	}

	async function deleteNote(id: number) {
		if (!confirm("Na pewno usunąć tę notatkę?")) return;
		try {
			await api.delete(`/${id}`);
			await loadNotes();
		} catch (err) {
			console.error("Błąd przy usuwaniu notatki:", err);
		}
	}

	async function switchFavourite(id: number) {
		try {
			const n = notes.value.find((n) => n.id === id);
			if (!n) return;
			await api.patch<Note>(`/${id}`, { isFavourite: !n.isFavourite });
			await loadNotes();
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

	const favNotes = computed(() => notes.value.filter((n) => n.isFavourite));
	const otherNotes = computed(() => notes.value.filter((n) => !n.isFavourite));

	loadNotes();
</script>
