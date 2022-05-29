import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from '../store';

interface UserState {
  email: String | null,
  username: String | null,
  messages: {message_id?: String, sender?: String, content?: String, timestamp?: String}[],
  keys: String[]
}

const initialState: UserState = {
  email: null,
  username: null,
  messages: [],
  keys: [],
}

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<{email?: String, username?: String}>) => {
      state.email = action.payload.email ?? null;
      state.username = action.payload.username ?? null;
    },
    setMessages: (state, action: PayloadAction<{message_id?: String, sender?: String, content?: String, timestamp?: String}[]>) => {
      state.messages = action.payload;
    }
  },
});

export const { setUser, setMessages } = userSlice.actions;
export const selectUser = (state: RootState) => state.user;

export default userSlice.reducer;
