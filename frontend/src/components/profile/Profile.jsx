import { useModeratedGroups } from "../../hooks/useModeratedGroups"

const Profile = () => {
  const { moderatedGroups, displayRole } = useModeratedGroups()
  
  return (
    <div>
      <h1>Profile</h1>
      <p>Display Role: {displayRole}</p>
      <p>Moderated Groups: {moderatedGroups.join(', ')}</p>
    </div>
  )
}

export default Profile