import create from 'zustand'

const useStore = create((set) => ({
  username: '',
  setUsername: (input) => set((state) => ({username: input}))
}))

export default useStore