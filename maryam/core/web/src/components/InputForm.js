import { InputGroup, InputLeftAddon, Input, InputRightElement, Button, HStack, FormControl } from '@chakra-ui/react'
import { Search2Icon } from '@chakra-ui/icons'
import { Field, Formik } from 'formik'
import React from 'react'

const InputForm = () => {
    const [dataObject, setDataObject] = React.useState([]);

    async function fetchData(query) {
        await fetch(`http://localhost:1313/api/modules?_module=iris&query=${query}`)
            .then(response => response.json())
            .then(data => setDataObject(data));
    }

    return (
        <Formik
            initialValues={{ query: '' }}
            onSubmit={(values) => {
                alert(values.query);
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

    )
}

export default InputForm