import React from 'react';
import { ChakraProvider } from '@chakra-ui/react'
import { Box, Text, LinkBox, LinkOverlay, HStack, FormControl, InputGroup, InputLeftAddon, InputRightElement, Button, Input } from '@chakra-ui/react';
import { Search2Icon } from '@chakra-ui/icons';
import { Field, Formik } from 'formik'
import './App.css';

function App() {
  const [dataObject, setDataObject] = React.useState([]);

  async function fetchData(query) {
    try {
      await fetch(`http://localhost:1313/api/modules?_module=iris&query=${query}`, {
        method: 'GET',
        headers: {
          'accept': 'application/json',
        },
      })
        .then(response => response.json())
        .then(data => setDataObject(data['output']['results']));
    }
    catch (error) {
      console.log(error);
    }
  }

  return (
    <ChakraProvider>
      <Formik
        initialValues={{ query: '' }}
        onSubmit={(values) => {
          // alert(values.query);
          fetchData(values.query);
        }}
      >
        {({ handleSubmit }) => (
          <form onSubmit={handleSubmit}>
            <HStack p='5' >
              <FormControl borderRightRadius={'full'}>

                <InputGroup boxShadow='base' borderRightRadius={'full'} w='xl'>
                  <InputLeftAddon children='iris -q' />

                  {/* <Input borderRadius={'full'} placeholder='Enter your query...' /> */}
                  <Field
                    as={Input}
                    name='query'
                    type='text'
                    placeholder='Enter your query...'
                    borderRightRadius={'full'}
                  />
                  <InputRightElement w='16' >
                    <Button borderRadius={'2xl'} size={'sm'} leftIcon={<Search2Icon />} colorScheme={'whatsapp'} type='submit'></Button>
                  </InputRightElement>
                </InputGroup>
              </FormControl>
              {/* <Text size='sm' p='5'>IRIS logo</Text> */}

            </HStack>
          </form>
        )}
      </Formik>

      <Box ml='40'>
        {
          dataObject.map((data) => {
            return (
              <LinkBox color={'blue'} p='2'>
                <LinkOverlay href={data.a} isExternal>
                  <Text textDecor='underline' fontSize='xl'>{data.t}</Text>
                  <Text fontSize='sm' color={'green'}>{data.c}</Text>
                  <Text fontSize='sm' color='gray'>{data.d}</Text>
                </LinkOverlay>
              </LinkBox>
            )
          })
        }
      </Box>
      {/* </VStack> */}

    </ChakraProvider>
  );
}

export default App;
