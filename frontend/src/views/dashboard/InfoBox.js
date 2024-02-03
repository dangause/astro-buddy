// ** MUI Imports
import Card from '@mui/material/Card'
import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'
import CardContent from '@mui/material/CardContent'
import { styled, useTheme } from '@mui/material/styles'

// Styled component for the triangle shaped background image
const TriangleImg = styled('img')({
  right: 0,
  bottom: 0,
  height: 170,
  position: 'absolute'
})

const InfoBox = () => {
  // ** Hook
  const theme = useTheme()
  const imageSrc = theme.palette.mode === 'light' ? 'triangle-light.png' : 'triangle-dark.png'

  return (
    <Card sx={{ position: 'relative' }}>
      <CardContent>
        <Typography variant='h6'>Quasar Query Machine</Typography>
        <Typography variant='bod3' style={{whiteSpace: 'pre-line'}} sx={{ letterSpacing: '0.25px' }}>
          Get the answer to any quasar related question.
        </Typography>
        <Typography variant="body1" style={{whiteSpace: 'pre-line'}} >
         This machine is fueled by arxiv articles in a vector database.
        </Typography>

      </CardContent>
    </Card>
  )
}

export default InfoBox
