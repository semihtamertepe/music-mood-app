import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux'
import type { RootState, AppDispatch } from './store'

// Dispatch'i özelleştir
export const useAppDispatch = () => useDispatch<AppDispatch>()
// Selector'u özelleştir
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector
