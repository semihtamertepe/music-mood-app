import { Navigate } from 'react-router-dom'
import { useAppSelector } from '../app/hooks'
import { ReactElement } from 'react'

interface Props {
  element: ReactElement
}

const PrivateRoute = ({ element }: Props) => {
  const token = useAppSelector((state) => state.auth.token)
  return token ? element : <Navigate to="/login" />
}

export default PrivateRoute
