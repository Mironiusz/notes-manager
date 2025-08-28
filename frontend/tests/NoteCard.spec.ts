import { mount } from "@vue/test-utils";
import NoteCard from "@/components/NoteCard.vue";

const note = {
  id: 1,
  title: "Hello",
  content: "Long content here",
  createdAt: "2025-08-28T12:34:56.000Z",
  isFavourite: true,
};

describe("NoteCard", () => {
  it("emits 'open' after clicking the card", async () => {
    const wrapper = mount(NoteCard, {
      props: { note, maxLength: 50 },
    });
    await wrapper.trigger("click");
    expect(wrapper.emitted("open")?.[0]).toEqual([1]);
  });

  it("emits 'toggle-favourite' after clicking the star", async () => {
    const wrapper = mount(NoteCard, {
      props: { note, maxLength: 50 },
    });
    await wrapper.find("button.note-card-fav").trigger("click");
    expect(wrapper.emitted("toggle-favourite")?.[0]).toEqual([1]);
  });

  it("emits 'delete' after clicking the close button", async () => {
    const wrapper = mount(NoteCard, {
      props: { note, maxLength: 50 },
    });
    await wrapper.find("button.note-card-delete").trigger("click");
    expect(wrapper.emitted("delete")?.[0]).toEqual([1]);
  });
});
