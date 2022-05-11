import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from '../store';

interface UserState {
  userId: String | null,
  username: String | null,
  messages: String[],
  keys: String[]
}

const initialState: UserState = {
  userId: null,
  username: null,
  messages: [],
  keys: [],
}

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<{userId?: String, username?: String}>) => {
      state.userId = action.payload.userId ?? null;
      state.username = action.payload.username ?? null;
    }
  },
});

export const { setUser } = userSlice.actions;
export const selectUser = (state: RootState) => state;

export default userSlice.reducer;
